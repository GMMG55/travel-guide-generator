#!/usr/bin/env python3
"""Create deterministic weather and seasonal travel advice."""

from datetime import datetime


SEASON_NAMES = {
    "spring": "春季",
    "summer": "夏季",
    "autumn": "秋季",
    "winter": "冬季",
}


def season_for_month(month, latitude=30.0):
    """Return meteorological season, respecting hemisphere."""
    northern = {
        12: "winter",
        1: "winter",
        2: "winter",
        3: "spring",
        4: "spring",
        5: "spring",
        6: "summer",
        7: "summer",
        8: "summer",
        9: "autumn",
        10: "autumn",
        11: "autumn",
    }
    season = northern[int(month)]
    if float(latitude) < 0:
        season = {
            "spring": "autumn",
            "summer": "winter",
            "autumn": "spring",
            "winter": "summer",
        }[season]
    return season


def build_season_tips(guide):
    """Build non-live seasonal and supplied-weather recommendations."""
    meta = guide.get("meta", {})
    start_date = meta.get("start_date")
    if not start_date:
        return []
    try:
        month = datetime.strptime(start_date, "%Y-%m-%d").month
    except ValueError:
        return []
    coordinates = meta.get("destination_coords") or [0, 30]
    latitude = coordinates[1] if len(coordinates) == 2 else 30
    season = season_for_month(month, latitude)
    tips = ["当前行程处于{}，出发前请再次核实临近天气。".format(SEASON_NAMES[season])]
    if season == "summer":
        tips.append("优先安排早晚户外活动，携带防晒、补水用品和轻便雨具。")
    elif season == "winter":
        tips.append("注意保暖与路面结冰，山区活动需准备防风层和防滑装备。")
    elif season == "spring":
        tips.append("昼夜温差可能较大，建议分层穿衣并关注花粉与降雨。")
    else:
        tips.append("早晚偏凉，建议携带薄外套并关注景区季节性开放时间。")

    for weather in guide.get("weather", []):
        condition = str(weather.get("condition", "")).lower()
        low = weather.get("temp_low")
        high = weather.get("temp_high")
        date_label = weather.get("date", "对应日期")
        if any(word in condition for word in ("雨", "rain", "storm", "雷")):
            tips.append("{}可能有降雨，为户外景点准备室内备选并防滑。".format(date_label))
        if high is not None and float(high) >= 32:
            tips.append("{}最高温较高，12:00-15:00减少长时间暴晒。".format(date_label))
        if low is not None and float(low) <= 5:
            tips.append("{}最低温偏低，夜间或登高活动需加强保暖。".format(date_label))
    return list(dict.fromkeys(tips))
