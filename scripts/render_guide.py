#!/usr/bin/env python3
"""Render structured travel-guide JSON with the bundled HTML template."""

import argparse
import json
from pathlib import Path

try:
    from .guide_utils import json_for_script, load_json, source_badges, source_index, text
    from .validate_guide import validate_guide
except ImportError:
    from guide_utils import json_for_script, load_json, source_badges, source_index, text
    from validate_guide import validate_guide


MODE_LABELS = {
    "walk": "步行",
    "bike": "骑行",
    "transit": "公共交通",
    "drive": "驾车",
}


def render_tags(guide):
    meta = guide.get("meta", {})
    preferences = guide.get("preferences", {})
    tags = [
        "{}天".format(meta.get("days", len(guide.get("days", [])))),
        "{}人".format(meta.get("travelers", 1)),
        preferences.get("group_type", "自由行"),
        preferences.get("pace", "balanced"),
    ]
    return "".join('<span class="tag">{}</span>'.format(text(tag)) for tag in tags if tag)


def render_language_attributes(meta):
    language = str(meta.get("language", "zh-CN"))
    root_language = language.lower().split("-", 1)[0]
    direction = ' dir="rtl"' if root_language in {"ar", "fa", "he", "ur"} else ""
    return 'lang="{}"{}'.format(text(language), direction)


def render_transport(guide, sources):
    records = guide.get("transport", [])
    if not records:
        return ""
    cards = []
    for record in records:
        cards.append(
            '<div class="t-item{}">{}<div class="t-title">{}</div>'
            '<div class="t-detail">{}</div><div class="t-price">{}</div>{}</div>'.format(
                " recommend" if record.get("recommended") else "",
                '<span class="badge">推荐</span>' if record.get("recommended") else "",
                text(record.get("title", record.get("mode", "交通"))),
                text(record.get("detail", "")),
                text(record.get("price", "")),
                source_badges(record.get("source_ids"), sources),
            )
        )
    return '<section class="transport-card"><h2>🚄 到达与当地交通</h2><div class="transport-grid">{}</div></section>'.format("".join(cards))


def render_hotels(guide, sources):
    records = guide.get("hotels", [])
    if not records:
        return ""
    cards = []
    for record in records:
        cards.append(
            '<div class="hotel-item"><div class="h-name">{}</div>'
            '<div class="h-price">{}</div><div class="h-desc">{}</div>'
            '<div class="h-rec">{}</div>{}</div>'.format(
                text(record.get("area", record.get("name", "住宿区域"))),
                text(record.get("price", "")),
                text(record.get("reason", "")),
                text(record.get("connection", "")),
                source_badges(record.get("source_ids"), sources),
            )
        )
    return '<section class="hotel-section"><h2>🏨 住宿推荐</h2><div class="hotel-grid">{}</div></section>'.format("".join(cards))


def render_route(route):
    if not route:
        return ""
    mode = MODE_LABELS.get(route.get("mode"), route.get("mode", "交通"))
    estimate = '<span class="estimate-tag">估算</span>' if route.get("estimated") else '<span class="amap-tag">高德实测</span>'
    return "{} {:.1f}km / {}分钟 {}".format(
        text(mode),
        float(route.get("distance_km", 0)),
        int(route.get("duration_min", 0)),
        estimate,
    )


def render_day_item(item, day_index, item_index, sources):
    key = "day-{}-item-{}".format(day_index + 1, item_index + 1)
    route = item.get("route_from_previous")
    source_html = source_badges(item.get("source_ids"), sources)
    coords = item.get("coords") or []
    coords_attr = ",".join(str(value) for value in coords)
    return (
        '<article class="spot itinerary-item" data-item-key="{key}" data-coords="{coords}">'
        '<div class="spot-head"><label class="item-toggle" title="标记完成">'
        '<input type="checkbox" class="item-check" data-key="{key}"></label>'
        '<div class="spot-icon">{icon}</div><div class="spot-main">'
        '<div class="spot-name"><span class="spot-title">{name}<span class="spot-price">{price}</span></span>'
        '<span class="spot-actions"><button type="button" class="favorite-btn" data-key="{key}" title="收藏">♡</button>'
        '<button type="button" class="edit-btn" data-key="{key}" aria-expanded="false">编辑</button></span></div>'
        '<div class="editable-schedule"><span class="schedule-display">{start}–{end}</span>'
        '<span class="item-edit-controls" hidden><input type="time" class="time-input start-time" '
        'data-key="{key}" value="{start}" aria-label="开始时间">–'
        '<input type="time" class="time-input end-time" data-key="{key}" value="{end}" aria-label="结束时间"></span>'
        '<span class="spot-transit">{route}</span></div>'
        '<div class="spot-desc">{description}</div>{sources}'
        '<label class="cost-editor item-edit-controls" hidden>预算 <input type="number" min="0" step="1" class="cost-input" '
        'data-key="{key}" value="{cost}"> {currency}</label>'
        '</div></div>{romance}{pitfall}</article>'
    ).format(
        key=key,
        coords=text(coords_attr),
        icon=text(item.get("icon", "📍")),
        name=text(item.get("name", "未命名行程")),
        price=text(item.get("price", "待核实")),
        start=text(item.get("start", "09:00")),
        end=text(item.get("end", "10:00")),
        route=render_route(route),
        description=text(item.get("description", "")),
        sources=source_html,
        cost=text(item.get("cost", 0)),
        currency=text(item.get("currency", "元")),
        romance='<div class="spot-romance">💕 {}</div>'.format(text(item["romance"])) if item.get("romance") else "",
        pitfall='<div class="pitfall">⚠️ {}</div>'.format(text(item["pitfall"])) if item.get("pitfall") else "",
    )


def render_days(guide, sources):
    cards = []
    for day_index, day in enumerate(guide.get("days", [])):
        items = day.get("items", [])
        route_names = " → ".join(item.get("name", "") for item in items)
        item_html = "".join(
            render_day_item(item, day_index, item_index, sources)
            for item_index, item in enumerate(items)
        )
        cards.append(
            '<section class="day-card" data-day="{day}"><div class="day-header d{color}">'
            '<div class="day-num">Day {day} · {date}</div><div class="day-title">{title}</div>'
            '<div class="day-route">{route}</div></div><div class="route-bar">'
            '<span class="dot"></span>{route}</div>{items}</section>'.format(
                day=text(day.get("day", day_index + 1)),
                date=text(day.get("date", "")),
                color=(day_index % 5) + 1,
                title=text(day.get("title", "")),
                route=text(route_names),
                items=item_html,
            )
        )
    return "".join(cards)


def render_foods(guide, sources):
    records = guide.get("foods", [])
    if not records:
        return ""
    cards = []
    for record in records:
        cards.append(
            '<div class="food-item"><div class="f-name">{}</div><div class="f-shop">{}</div>'
            '<div class="f-price">{}</div><div class="f-note">{}</div>{}</div>'.format(
                text(record.get("name", "")),
                text(record.get("shop", "")),
                text(record.get("price", "")),
                text(record.get("reason", "")),
                source_badges(record.get("source_ids"), sources),
            )
        )
    return '<section class="food-section"><h2>🍜 美食推荐</h2><div class="food-grid">{}</div></section>'.format("".join(cards))


def render_avoid(guide, sources):
    records = guide.get("avoid", [])
    if not records:
        return ""
    items = []
    for index, record in enumerate(records):
        items.append(
            '<div class="avoid-item"><div class="a-num">{}</div><div>'
            '<span class="a-wrong">{}</span> → <span class="a-right">{}</span>{}</div></div>'.format(
                index + 1,
                text(record.get("wrong", "")),
                text(record.get("right", "")),
                source_badges(record.get("source_ids"), sources),
            )
        )
    return '<section class="avoid-section"><h2>⚠️ 避坑清单</h2><div class="avoid-list">{}</div></section>'.format("".join(items))


def render_budget(guide):
    budget = guide.get("budget", {})
    profiles = budget.get("profiles", {})
    selected = budget.get("selected") or guide.get("preferences", {}).get("budget_level", "comfortable")
    profile = profiles.get(selected) or next(iter(profiles.values()), {})
    categories = profile.get("categories", {})
    if not categories:
        return ""
    rows = "".join(
        '<div class="budget-row"><span>{}</span><span>{}</span></div>'.format(text(name), text(value))
        for name, value in categories.items()
    )
    total = profile.get("total", sum(value for value in categories.values() if isinstance(value, (int, float))))
    return (
        '<section class="budget-card"><h2>💰 预算估算 · {}</h2><div>{}'
        '<div class="budget-total">计划预算：<span id="baseBudget">{}</span> '
        '<span class="currency-label">{}</span><br><small>本地编辑合计：'
        '<span id="liveBudget">0</span> <span class="currency-label">{}</span></small></div></div></section>'
    ).format(text(selected), rows, text(total), text(guide.get("meta", {}).get("currency", "CNY")), text(guide.get("meta", {}).get("currency", "CNY")))


def render_tips(guide):
    tips = guide.get("tips", []) + guide.get("season_tips", [])
    if not tips:
        return ""
    return '<section class="tips-card"><h2>🧳 出行 Tips</h2><div>{}</div></section>'.format(
        "".join('<div class="tip-item"><span>✓</span><span>{}</span></div>'.format(text(tip)) for tip in tips)
    )


def render_meta_sections(guide, report, sources):
    preferences = guide.get("preferences", {})
    preference_parts = []
    labels = {
        "budget_level": "预算",
        "pace": "节奏",
        "group_type": "人群",
        "interests": "兴趣",
        "dietary": "饮食",
        "accessibility": "无障碍",
        "transport": "交通偏好",
    }
    for key, label in labels.items():
        value = preferences.get(key)
        if value:
            display = "、".join(str(item) for item in value) if isinstance(value, list) else value
            preference_parts.append('<span class="meta-chip"><b>{}</b> {}</span>'.format(text(label), text(display)))
    weather_rows = []
    for weather in guide.get("weather", []):
        weather_rows.append(
            '<div class="weather-item"><b>{}</b><span>{}</span><span>{}–{}℃</span>{}{}</div>'.format(
                text(weather.get("date", "")),
                text(weather.get("condition", "待核实")),
                text(weather.get("temp_low", "?")),
                text(weather.get("temp_high", "?")),
                source_badges(weather.get("source_ids"), sources),
                '<div class="weather-backup">室内备选：{}</div>'.format(text(weather["backup_plan"])) if weather.get("backup_plan") else "",
            )
        )
    issues = report.get("errors", []) + report.get("conflicts", []) + report.get("warnings", [])
    issue_rows = "".join(
        '<li class="issue-{}"><b>{}</b> {} <code>{}</code></li>'.format(
            text(item.get("level", "warning")), text(item.get("code", "CHECK")), text(item.get("message", "")), text(item.get("path", ""))
        )
        for item in issues
    )
    source_rows = "".join(
        '<li><span class="source-type">{}</span>{}</li>'.format(
            text(source.get("type", "search")),
            source_badges([source_id], sources),
        )
        for source_id, source in sources.items()
    )
    sections = [
        '<section class="tool-card"><div class="toolbar"><button type="button" id="printGuide">🖨️ 打印/PDF</button>'
        '<button type="button" id="exportState">💾 导出修改</button><button type="button" id="resetState">↺ 清除本地修改</button>'
        '<span id="saveStatus">修改仅保存在本浏览器</span></div></section>',
        '<section class="preferences-section"><h2>🎛️ 本次旅行偏好</h2><div class="meta-chips">{}</div></section>'.format("".join(preference_parts)),
    ]
    if weather_rows:
        sections.append('<section class="weather-section"><h2>🌦️ 天气与季节</h2><div>{}</div></section>'.format("".join(weather_rows)))
    if issues:
        sections.append(
            '<section class="quality-section"><h2>🩺 行程质量检查</h2><div class="quality-summary">错误 {} · 冲突 {} · 提醒 {}</div>{}</section>'.format(
            len(report.get("errors", [])),
            len(report.get("conflicts", [])),
            len(report.get("warnings", [])),
            '<ul class="issue-list">{}</ul>'.format(issue_rows),
            )
        )
    if source_rows:
        sections.append('<section class="sources-section"><h2>🔎 信息来源与核实日期</h2><ul>{}</ul></section>'.format(source_rows))
    return "".join(sections)


def render_html(guide, template_text, report=None):
    report = report or validate_guide(guide)
    sources = source_index(guide)
    meta = guide.get("meta", {})
    replacements = {
        "{{LANG_ATTR}}": render_language_attributes(meta),
        "{{TITLE}}": text(meta.get("title", "旅游攻略")),
        "{{EMOJIS}}": text(meta.get("emojis", "🌍🧭✨")),
        "{{SUBTITLE}}": text(meta.get("subtitle", "为这一次出发认真规划")),
        "{{TAGS}}": render_tags(guide),
        "{{META_SECTIONS}}": render_meta_sections(guide, report, sources),
        "{{TRANSPORT_SECTION}}": render_transport(guide, sources),
        "{{HOTEL_SECTION}}": render_hotels(guide, sources),
        "{{DAILY_ITINERARY}}": render_days(guide, sources),
        "{{FOOD_SECTION}}": render_foods(guide, sources),
        "{{AVOID_SECTION}}": render_avoid(guide, sources),
        "{{BUDGET_SECTION}}": render_budget(guide),
        "{{TIPS_SECTION}}": render_tips(guide),
        "{{FOOTER_TEXT}}": text(meta.get("footer", "信息会变化，预订与出发前请再次核实。")),
        "{{GUIDE_DATA}}": json_for_script(guide),
    }
    output = template_text
    for placeholder, value in replacements.items():
        output = output.replace(placeholder, value)
    if "{{" in output:
        raise ValueError("HTML 模板仍有未填充占位符")
    return output


def render_file(guide, output_path, template_path=None, allow_invalid=False):
    report = validate_guide(guide)
    if not report["valid"] and not allow_invalid:
        raise ValueError("攻略校验失败，使用 --allow-invalid 可强制渲染")
    template = Path(template_path or Path(__file__).parents[1] / "assets" / "template.html")
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_html(guide, template.read_text(encoding="utf-8"), report), encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description="从结构化 JSON 渲染旅游攻略 HTML")
    parser.add_argument("input", help="攻略 JSON 文件")
    parser.add_argument("--output", required=True, help="输出 HTML 文件")
    parser.add_argument("--template", help="自定义 HTML 模板")
    parser.add_argument("--allow-invalid", action="store_true")
    args = parser.parse_args()
    try:
        report = render_file(load_json(args.input), args.output, args.template, args.allow_invalid)
        print(json.dumps({"status": "ok", "output": args.output, "report": report}, ensure_ascii=False, indent=2))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "error", "message": str(error)}, ensure_ascii=False))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
