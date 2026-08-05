from ..llm import chat_raw
import json


STATE_EXTRACT_PROMPT = """

你是一个旅行信息提取器。请从用户输入中提取旅行相关信息。只输出JSON。

字段：

destination:旅行目的地

days:旅行天数

budget:预算

start_date:出发日期

如果没有对应信息，返回null。

用户输入：

{message}

"""


def extract_state(message):

    prompt = STATE_EXTRACT_PROMPT.format(
        message=message
    )

    response = chat_raw(prompt)

    # print("======STATE EXTRACT RAW======")
    # print(response)
    # print("============================")

    return json.loads(response)