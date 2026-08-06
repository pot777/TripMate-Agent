from datetime import datetime, timedelta
import re
import dateparser


def normalize_date(date_text: str):

    if not date_text:
        return None

    today = datetime.today().date()


    # 先尝试dateparser
    result = dateparser.parse(
        date_text
    )

    if result:
        return str(result.date())


    # 今天
    if date_text == "今天":
        return str(today)


    # 明天
    if date_text == "明天":
        return str(today + timedelta(days=1))


    # 后天
    if date_text == "后天":
        return str(today + timedelta(days=2))


    # 下周X
    weekday_map = {
        "一":0,
        "二":1,
        "三":2,
        "四":3,
        "五":4,
        "六":5,
        "日":6
    }


    if date_text.startswith("下周"):

        day = date_text[-1]

        if day in weekday_map:

            target = weekday_map[day]

            days = (
                7 - today.weekday()
                + target
            )

            return str(
                today + timedelta(days=days)
            )


    # 下下周X

    if date_text.startswith("下下周"):

        day = date_text[-1]

        if day in weekday_map:

            target = weekday_map[day]

            days = (
                14 - today.weekday()
                + target
            )

            return str(
                today + timedelta(days=days)
            )


    # 下个月X号

    match = re.match(
        r"下个月([0-9一二三四五六七八九十]+)[号日]?",
        date_text
    )

    if match:

        day_text = match.group(1)

        num_map = {
            "一":1,
            "二":2,
            "三":3,
            "四":4,
            "五":5,
            "六":6,
            "七":7,
            "八":8,
            "九":9,
            "十":10
        }

        day = (
            int(day_text)
            if day_text.isdigit()
            else num_map.get(day_text)
        )

        if day:

            year = today.year
            month = today.month + 1

            if month == 13:
                year += 1
                month = 1

            return str(
                datetime(
                    year,
                    month,
                    day
                ).date()
            )


    # 8月15号

    match = re.match(
        r"([0-9]+)月([0-9]+)[号日]?",
        date_text
    )

    if match:

        month = int(match.group(1))
        day = int(match.group(2))

        year = today.year

        return str(
            datetime(
                year,
                month,
                day
            ).date()
        )


    return date_text


def can_query_weather(target_date, days=4):

    today = datetime.today().date()

    try:
        target = datetime.strptime(
            target_date,
            "%Y-%m-%d"
        ).date()

    except:

        return False


    delta = (target - today).days

    return 0 <= delta <= days