from .weather import get_weather
from .attraction import search_attractions


TOOLS = {
    "get_weather": {
        "description": "查询指定城市的天气信息",
        "parameters":{
            "city":"string"
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