def get_weather(city: str):

    fake_weather = {
        "成都": {
            "weather": "多云",
            "temperature": "28℃",
            "suggestion": "适合户外游玩，建议携带雨具"
        },
        "上海": {
            "weather": "小雨",
            "temperature": "30℃",
            "suggestion": "建议携带雨伞"
        },
        "北京": {
            "weather": "晴",
            "temperature": "32℃",
            "suggestion": "注意防晒"
        }
    }

    return fake_weather.get(
        city,
        {
            "weather": "未知",
            "temperature": "未知",
            "suggestion": "暂无天气信息"
        }
    )