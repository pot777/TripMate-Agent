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
5. 不要重复调用已经获得结果的工具。
6. 如果工具返回available=false或error信息：认为该工具结果不可用，不要重复调用；根据已有信息继续完成任务。
7. 如果天气信息不可用：生成旅行方案时不要假设具体天气，可以给出通用出行建议。
8. 如果需要景点推荐、旅游经验、适合人群、游玩建议等静态旅游知识：调用retrieve_travel_info。

天气查询规则：

1. 如果用户提供明确旅行日期：
   调用get_weather，并传递date参数。

2. 如果用户询问当前天气：
   调用get_weather，只传递city参数。

3. 如果生成旅行方案：
   优先查询旅行日期范围内天气，用于调整每日安排。

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


def run_agent(message,session_id="default"):
    
    add_message(session_id,"user",message)

    extracted = extract_state(message)

    # if extracted.get("start_date"):
    #     extracted["start_date"] = normalize_date(
    #         extracted["start_date"]
    #     )

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

    for step in range(MAX_STEPS):

        print("================")
        print(f"Agent Step {step+1}")
        print("================")


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


        if decision.action=="tool":

            tool_result = execute_tool(
                decision.tool,
                decision.arguments
            )

            add_message(session_id,"tool",str(tool_result))

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