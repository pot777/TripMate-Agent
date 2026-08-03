# agent.py
from .llm import chat_with_llm, chat_raw
from .tools.registry import TOOLS
import json
from .models import AgentAction


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

{
    "action":"tool",
    "tool":"工具名称",
    "arguments":{}
}


2. need_information

表示用户信息不足，需要询问。

格式：

{
    "action":"need_information",
    "message":"需要用户补充的信息"
}


3. final

表示无需调用工具，可以直接回答。

格式：

{
    "action":"final",
    "answer":"回答内容"
}


你可以调用以下工具：
{tools}

判断规则：
1. 如果用户需求无法完成，需要的信息缺失：输出 need_information。
2. 如果用户询问天气：调用 get_weather。
3. 如果用户需要旅行规划且已有目的地、天数、预算：可以调用 search_attractions。
4. 如果无需工具：输出 final。

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


    result = tool["function"](**arguments)

    return result


def check_information(message):

    missing = []

    if "天" not in message:
        missing.append("旅行天数")

    if "预算" not in message:
        missing.append("预算")

    return missing


def run_agent(message):


    # Step1 Planner决定下一步

    decision = decide_action(message)


    print("================")
    print("Agent Decision:")
    print(decision)
    print("================")


    # Step2 信息不足

    if decision.action=="need_information":

        return {
            "status":"need_information",
            "message":decision.message
        }


    # Step3 调用工具

    if decision.action=="tool":


        tool_result = execute_tool(
            decision.tool,
            decision.arguments
        )


        print("Tool Observation:")
        print(tool_result)



        final_prompt=f"""

用户需求：

{message}


工具返回：

{tool_result}


请根据工具信息生成完整旅行方案。

要求：

1. 必须使用工具返回的信息；
2. 不要编造工具不存在的信息；
3. 输出完整旅行方案JSON。

"""


        return chat_with_llm(final_prompt)



    # Step4 直接回答

    if decision.action=="final":

        return decision.answer


