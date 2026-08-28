# llm.py
import json
from typing import TypeVar

from openai import OpenAI
from pydantic import BaseModel, ValidationError

from .config import DEEPSEEK_API_KEY
from .models import TravelPlan

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
    timeout=60.0,
    max_retries=1
)


class LLMResponseError(RuntimeError):
    """The LLM responded, but its structured content was unusable."""


ModelT = TypeVar("ModelT", bound=BaseModel)


def _strip_json_fence(content: str) -> str:
    content = content.strip()
    if not content.startswith("```"):
        return content

    lines = content.splitlines()
    if lines:
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def parse_structured_response(content, model_type: type[ModelT]) -> ModelT:
    if content is None or not str(content).strip():
        raise LLMResponseError("LLM returned empty content")

    cleaned = _strip_json_fence(str(content))
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise LLMResponseError("LLM returned invalid JSON") from exc

    try:
        return model_type.model_validate(data)
    except ValidationError as exc:
        raise LLMResponseError("LLM response failed schema validation") from exc


def _completion_content(messages):
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages
    )
    if not response.choices:
        raise LLMResponseError("LLM returned no choices")
    return response.choices[0].message.content


def chat_with_llm(message: str):
    messages = [
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

    for attempt in range(2):
        content = _completion_content(messages)
        try:
            return parse_structured_response(content, TravelPlan)
        except LLMResponseError:
            if attempt == 1:
                raise


def chat_raw(message: str):
    content = _completion_content(
        [
            {
                "role": "user",
                "content": message
            }
        ]
    )
    if content is None or not content.strip():
        raise LLMResponseError("LLM returned empty content")
    return content
