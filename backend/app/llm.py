from openai import OpenAI
from .config import DEEPSEEK_API_KEY


client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)


def chat_with_llm(message: str):

    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {
                    "role": "system",
                    "content": "你是一名资深旅行规划助手。你的任务是根据用户提供的目的地、旅行时间、预算和偏好生成个性化旅行方案。要求：1. 给出每日行程安排；2. 包括交通建议；3. 推荐特色美食；4. 给出预算估算；5. 如果用户信息不足，需要主动询问补充信息。"
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"模型调用失败：{str(e)}"