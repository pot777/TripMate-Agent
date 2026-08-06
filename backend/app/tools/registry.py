# registry.py
from .weather import get_weather
from .attraction import search_attractions


TOOLS = {
    "get_weather": {
        "description":
        """
        查询指定城市天气。支持查询今天和未来4天内天气，超过范围无法获取准确预测。
        如果用户提供旅行日期，查询对应日期天气；
        如果未提供日期，查询当前天气。
        """,
        "parameters":{
            "city":"string",
            "date":"optional string"
        },
        "function": get_weather
    },

    "search_attractions": {
        "description":"查询城市热门景点",
        "parameters":{
            "city":"string"
        },
        "function":search_attractions
    }

}