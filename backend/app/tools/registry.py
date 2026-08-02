from .weather import get_weather


TOOLS = {
    "get_weather": {
        "description": "查询指定城市的天气信息",
        "function": get_weather
    }
}