from .llm import chat_with_llm
from .tools.weather import get_weather

def check_information(message):

    missing = []

    if "天" not in message:
        missing.append("旅行天数")

    if "预算" not in message:
        missing.append("预算")

    return missing


def run_agent(message: str):

    missing = check_information(message)

    if missing:
        return {
            "status": "need_information",
            "message": f"请补充：{','.join(missing)}"
        }
    
    # 简单判断用户是否需要天气
    if "天气" in message:

        # 简单提取城市
        city = None

        for c in ["成都", "上海", "北京"]:
            if c in message:
                city = c

        if city:
            weather_info = get_weather(city)
            # print("调用天气工具:", weather_info)

            enhanced_message = f"""
用户需求：
{message}

你已经调用天气工具获得以下实时信息：

天气：
{weather_info['weather']}

温度：
{weather_info['temperature']}

出行建议：
{weather_info['suggestion']}

要求：
1. 根据天气调整行程安排；
2. 如果天气影响户外活动，请给出替代建议；
3. 输出完整旅行方案。
"""

            return chat_with_llm(enhanced_message)


    # 普通请求直接调用LLM
    return chat_with_llm(message)