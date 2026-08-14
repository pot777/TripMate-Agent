# agent.py
from .llm import chat_with_llm, chat_raw
from .tools.registry import TOOLS
import json
from .models import AgentAction
MAX_STEPS = 10
from .memory.store import (
    add_message,
    get_history
)
from .memory.extractor import extract_state
from .memory.state import (
    get_state,
    update_state
)
from .utils.date_parser import normalize_date

def build_tool_description():

    descriptions=[]

    for name, info in TOOLS.items():

        descriptions.append(
            f"""
工具名称:
{name}

功能:
{info['description']}

参数:
{info['parameters']}
"""
        )

    return "\n".join(descriptions)


AGENT_SYSTEM_PROMPT = """

你是一个旅行规划Agent。

你的任务是理解用户需求，并决定下一步行动。

你有三种Action：

1. tool

表示需要调用外部工具。

格式：

{{
    "action":"tool",
    "tool":"工具名称",
    "arguments":{{}}
}}


2. need_information

表示用户信息不足，需要询问。

格式：

{{
    "action":"need_information",
    "message":"需要用户补充的信息"
}}


3. final

表示无需调用工具，可以直接回答。

格式：

{{
    "action":"final",
    "answer":"回答内容"
}}


4. generate_plan

表示已经获取了制定旅行方案所需的信息，需要生成结构化旅行计划。

格式：

{{
    "action":"generate_plan"
}}


你可以调用以下工具：
{tools}

判断规则：

1. 如果旅行规划缺少目的地、天数或预算，输出 need_information。
2. 如果缺少完成任务所需的外部信息，输出 tool。
3. 如果已经获得足够信息并需要生成旅行方案，输出 generate_plan。
4. 如果用户只询问天气、景点等简单信息，获得工具结果后输出 final。
5. 不要重复执行已经完成的工具任务。即使参数表述不同，只要目的和信息需求相同，也不要再次调用相同工具。
6. 如果工具返回error信息：认为该工具执行失败，不要重复调用相同工具；根据当前任务判断是否可以调用其他工具继续完成任务。
7. 如果retrieve_travel_info返回available=false：表示当前RAG知识库没有足够相关的信息。此时不要再次调用retrieve_travel_info，应调用search_web作为fallback查询外部旅游信息。调用 search_web 查询旅游信息时，必须同时传递目标城市 city 和搜索 query。
8. 如果 retrieve_travel_info 已经返回 available=true，则认为旅游知识检索已完成，不要再次调用 retrieve_travel_info；应继续查询其他必要信息或生成旅行方案。
9. 如果用户明确表示“不想太累、轻松、少走路”等低强度偏好，调用 retrieve_travel_info 时将 exclude_high_intensity 设置为 true。
10. 如果search_web返回available=false：表示外部搜索也没有获得有效信息，不要重复搜索；根据已有信息继续回答或生成旅行方案。
11. 如果天气信息不可用：生成旅行方案时不要假设具体天气，可以给出通用出行建议。

天气查询规则：

1. 如果用户提供明确旅行日期：调用get_weather，并传递date参数。
2. 如果用户询问当前天气：调用get_weather，只传递city参数。
3. 如果生成旅行方案：优先查询旅行日期范围内天气，用于调整每日安排。

个性化检索规则：

1. 当前旅行状态中的 travelers、preferences、interests 属于用户个性化需求。
2. 调用 retrieve_travel_info 时，应结合 destination、travelers、preferences、interests 生成具体的 query。
3. 不要只使用城市名或“景点推荐”作为 query。
4. 如果某个个性化字段为空，不要自行补充或猜测。
5. 如果 RAG 查询失败并调用 search_web，Web Search 的 query 同样应保留这些用户偏好。

只能输出JSON，不要输出其他内容。

"""


def decide_action(message):

    prompt = f"""
{AGENT_SYSTEM_PROMPT.format(
    tools=build_tool_description()
)}


用户输入：

{message}

"""


    response = chat_raw(prompt)

    # print("======LLM RAW OUTPUT======")
    # print(response)
    # print("==========================")

    data = json.loads(response)

    action = AgentAction(**data)

    return action


def execute_tool(tool_name, arguments):

    tool = TOOLS.get(tool_name)

    if tool is None:
        return {
            "error": f"tool {tool_name} not found"
        }

    try:
        return tool["function"](**arguments)

    except Exception as e:
        return {
            "error": f"tool {tool_name} execution failed: {str(e)}"
        }


def build_tool_call_key(tool_name, arguments):

    arguments_json = json.dumps(
        arguments,
        sort_keys=True,
        ensure_ascii=False
    )

    return f"{tool_name}:{arguments_json}"


def run_agent(message,session_id="default"):
    
    add_message(session_id,"user",message)

    extracted = extract_state(message)

    update_state(session_id,**extracted)

    history = get_history(session_id)
    # print("Memory:")
    # print(history)
    state = get_state(session_id)
    print("State:")
    print(state)

    current_message = f"""

当前旅行状态：

{state}


历史对话：

{history}


"""

    completed_tasks = {
        "travel_info": False,
        "web_search": False
    }

    executed_calls = set()

    for step in range(MAX_STEPS):

        # print("================")
        print(f"Agent Step {step+1}")
        # print("================")


        decision = decide_action(current_message)


        print("Agent Decision:")
        print(decision)



        if decision.action=="need_information":

            answer = {
                "status":"need_information",
                "message":decision.message
            }

            add_message(session_id,"assistant",str(answer))

            return answer


        if decision.action == "tool":

            tool_call_key = build_tool_call_key(
                decision.tool,
                decision.arguments
            )

            # RAG 已经成功获得旅游知识，不允许重复检索
            if (
                decision.tool == "retrieve_travel_info"
                and completed_tasks["travel_info"]
            ):

                tool_result = {
                    "error": "travel_info_already_available",
                    "message": "本轮已经获得有效旅游知识，请继续其他必要步骤或生成旅行方案。"
                }

            # 完全相同的工具调用不重复执行
            elif tool_call_key in executed_calls:

                tool_result = {
                    "error": "duplicate_tool_call",
                    "message": "该工具已使用相同参数执行过，请根据已有结果继续判断。"
                }

            else:

                executed_calls.add(tool_call_key)

                tool_result = execute_tool(
                    decision.tool,
                    decision.arguments
                )

                if (
                    decision.tool == "retrieve_travel_info"
                    and isinstance(tool_result, dict)
                    and tool_result.get("available") is True
                ):

                    completed_tasks["travel_info"] = True


            add_message(
                session_id,
                "tool",
                str(tool_result)
            )

            print("Tool Observation:")
            print(tool_result)

            current_message += f"""

Tool Observation:

{tool_result}

请根据以上Observation继续判断下一步。

"""
            continue


        if decision.action == "generate_plan":

            final_prompt = f"""
请根据以下用户需求和工具Observation生成完整旅行方案：

{current_message}

要求：
1. 必须使用所有已经获得的工具信息；
2. 景点信息应体现在每日行程中；
3. 天气信息应影响活动安排，并给出对应出行建议；
4. 不要编造工具未提供的实时信息；
5. 严格输出TravelPlan要求的JSON格式。
"""

            answer = chat_with_llm(final_prompt)

            add_message(session_id,"assistant",str(answer))

            return answer


        if decision.action=="final":

            add_message(session_id,"assistant",decision.answer)

            return decision.answer


    answer={
        "status":"error",
        "message":"Agent reached maximum steps"
    }

    add_message(session_id,"assistant",str(answer))

    return answer