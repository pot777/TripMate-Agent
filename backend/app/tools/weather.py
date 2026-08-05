import requests

from ..config import AMAP_API_KEY



def get_weather(city:str,date=None):

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
            "message": "高德天气仅支持未来4天预测"
        }



    except Exception as e:

        return {
            "error":str(e)
        }