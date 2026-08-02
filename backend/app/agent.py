from .llm import chat_with_llm, chat_raw
from .tools.weather import get_weather
from .tools.registry import TOOLS
import json

AGENT_SYSTEM_PROMPT = """

你是一个旅行规划Agent。

你可以使用以下工具：

工具：
get_weather:
查询城市天气。

如果需要调用工具，请输出JSON：

{
    "action":"tool",
    "tool":"工具名称",
    "arguments":{
    }
}


如果不需要工具，直接回答：

{
    "action":"final",
    "answer":"你的回答"
}

只能输出JSON。

"""


def decide_action(message):

    prompt = f"""
{AGENT_SYSTEM_PROMPT}


用户输入：

{message}

"""


    response = chat_raw(prompt)

    # print("======LLM RAW OUTPUT======")
    # print(response)
    # print("==========================")

    return json.loads(response)


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


    missing = check_information(message)


    if missing:
        return {
            "status":"need_information",
            "message":
            f"请补充：{','.join(missing)}"
        }


    decision = decide_action(message)


    if decision["action"]=="tool":


        tool_result = execute_tool(
            decision["tool"],
            decision["arguments"]
        )


        final_prompt=f"""

用户需求：

{message}


工具返回：

{tool_result}


请严格基于工具返回的信息生成旅行方案。

要求：

1. 在旅行方案中体现工具返回的信息；
2. 根据工具返回的信息调整每日活动安排；
3. 如果工具返回的信息不适合户外活动，需要提供替代方案；
4. destination字段中包含当前工具返回的信息摘要；
5. 不要忽略工具返回的信息。

输出完整旅行方案JSON。

"""

        print("Agent Action:", decision)
        print("Tool Result:", tool_result)


        return chat_with_llm(final_prompt)



    else:

        return decision["answer"]


if __name__ == "__main__":

    result = execute_tool(
        "get_weather",
        {
            "city":"成都"
        }
    )

    print(result)