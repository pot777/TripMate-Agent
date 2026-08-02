from openai import OpenAI
from .config import DEEPSEEK_API_KEY
import json
from .models import TravelPlan

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
                    "content": """
                    你是一名资深旅行规划助手。你的任务是根据用户提供的目的地、旅行时间、预算和偏好生成个性化旅行方案。
            
                    要求：
                    1. 给出每日行程安排；
                    2. 包括交通建议；
                    3. 推荐特色美食；
                    4. 给出预算估算；
                    5. 如果用户信息不足，需要主动询问补充信息。
                    
                    请严格按照以下JSON格式输出，不要输出额外解释：
                    
                    {
                        "destination":"",
                        "days":0,
                        "budget":0,
                        "schedule":[
                            {
                            "day":0,
                            "title":"",
                            "activities":[],
                            "transportation":"",
                            "accommodation_suggestion":""
                            }
                        ],
                        "food":[],
                        "budget_breakdown":{
                            "transportation":0,
                            "accommodation":0,
                            "food":0,
                            "entertainment":0,
                            "misc":0,
                            "total_estimated":0
                        }
                    }
                    """
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        content = response.choices[0].message.content
        data = json.loads(content)
        plan = TravelPlan(**data)
        return plan

    except Exception as e:
        return f"模型调用失败：{str(e)}"


def chat_raw(message: str):

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response.choices[0].message.content