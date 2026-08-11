# registry.py
from .weather import get_weather
from .attraction import search_attractions
from .rag import retrieve_travel_info


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
    },

    "retrieve_travel_info": {

        "description":
        """
        查询旅游知识库。
        用于获取景点介绍、
        适合人群、
        游玩强度、
        旅游建议等静态旅游信息。
        """,

        "parameters":{
            "city":"string",
            "query":"string"
        },

        "function":retrieve_travel_info
    }

}