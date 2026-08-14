from ..llm import chat_raw
import json


STATE_EXTRACT_PROMPT = """

你是一个旅行信息提取器。请从用户输入中提取旅行相关信息。只输出JSON。

字段：

destination:旅行目的地
days:旅行天数
budget:预算
start_date:出发日期
travelers：同行人员，例如父母、老人、孩子、情侣、朋友
preferences：旅行方式偏好，例如轻松、少走路、不爬山、节奏慢
interests：兴趣偏好，例如历史文化、自然风光、美食、摄影、动物
travelers、preferences、interests 必须输出JSON数组，没有提到时输出空数组。
只能提取用户明确表达的信息，不要自行推测。

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