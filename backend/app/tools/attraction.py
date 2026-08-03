def search_attractions(city: str):

    attractions = {

        "成都": [
            "大熊猫基地",
            "宽窄巷子",
            "武侯祠",
            "都江堰",
            "青城山"
        ],

        "上海": [
            "外滩",
            "东方明珠",
            "豫园"
        ],

        "北京": [
            "故宫",
            "长城",
            "颐和园"
        ]

    }

    return {
        "city": city,
        "attractions": attractions.get(city, [])
    }