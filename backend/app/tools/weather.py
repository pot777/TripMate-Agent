# weather.py
import requests

from ..config import AMAP_API_KEY
from ..utils.date_parser import can_query_weather


def get_weather(city:str,date=None):

    # 未来天气查询范围判断

    if date and not can_query_weather(date):

        return {
            "city": city,
            "date": date,
            "available": False,
            "message": "距离出发日期过远，无法获取准确天气"
        }

    url = "https://restapi.amap.com/v3/weather/weatherInfo"

    params = {
        "key": AMAP_API_KEY,
        "city": city,
        "extensions": "all" if date else "base"
    }


    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data=response.json()
        # print(data)


        if data["status"]!="1":

            return {
                "error":data.get("info")
            }


        if not date:

            weather = data["lives"][0]

            return {
                "city": weather["city"],
                "date": "today",
                "available": True,
                "weather": weather["weather"],
                "temperature": weather["temperature"]+"℃",
                "wind": weather["winddirection"],
                "humidity": weather["humidity"]
            }
        

        # 未来天气

        forecasts = data["forecasts"][0]["casts"]


        for forecast in forecasts:

            if forecast["date"] == date:

                return {
                    "city": city,
                    "date": date,
                    "available": True,
                    "weather_day": forecast["dayweather"],
                    "weather_night": forecast["nightweather"],
                    "temperature_day": forecast["daytemp"]+"℃",
                    "temperature_night": forecast["nighttemp"]+"℃",
                    "wind": forecast["daywind"]
                }

        return {
            "city": city,
            "date": date,
            "available": False,
            "message": "未查询到该日期天气信息"
        }



    except Exception as e:

        return {
            "error":str(e)
        }