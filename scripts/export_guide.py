#!/usr/bin/env python3
"""Export a structured guide to Markdown, iCalendar and GeoJSON."""

import argparse
import json
from pathlib import Path

try:
    from .guide_utils import load_json, write_json
except ImportError:
    from guide_utils import load_json, write_json


def markdown_text(guide):
    meta = guide.get("meta", {})
    lines = ["# {}".format(meta.get("title", "旅游攻略")), ""]
    lines.append(
        "- 目的地：{}".format(meta.get("destination", ""))
    )
    lines.append("- 日期：{}".format(meta.get("start_date", "")))
    lines.append("- 人数：{}".format(meta.get("travelers", 1)))
    lines.append("")
    for day in guide.get("days", []):
        lines.extend(
            [
                "## Day {} · {}".format(day.get("day", ""), day.get("title", "")),
                "",
            ]
        )
        for item in day.get("items", []):
            line = "- {}–{} **{}**".format(
                item.get("start", ""), item.get("end", ""), item.get("name", "")
            )
            if item.get("description"):
                line += " — {}".format(item["description"])
            lines.append(line)
        lines.append("")
    if guide.get("tips"):
        lines.extend(["## 出行提示", ""])
        lines.extend("- {}".format(tip) for tip in guide["tips"])
        lines.append("")
    lines.append("## 数据来源")
    lines.append("")
    for source in guide.get("sources", []):
        label = source.get("title", source.get("id", "来源"))
        url = source.get("url")
        checked = source.get("checked_at", "未注明")
        lines.append("- [{}]({})（核实：{}）".format(label, url, checked) if url else "- {}（核实：{}）".format(label, checked))
    return "\n".join(lines).rstrip() + "\n"


def ics_escape(value):
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def ics_text(guide):
    meta = guide.get("meta", {})
    timezone = meta.get("timezone", "Asia/Shanghai")
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Travel Guide Generator//CN",
        "CALSCALE:GREGORIAN",
    ]
    slug = meta.get("destination", "trip")
    for day in guide.get("days", []):
        date_value = str(day.get("date", "")).replace("-", "")
        for index, item in enumerate(day.get("items", [])):
            start = str(item.get("start", "00:00")).replace(":", "") + "00"
            end = str(item.get("end", "00:00")).replace(":", "") + "00"
            uid = "{}-{}-{}@travel-guide-generator".format(slug, date_value, index)
            lines.extend(
                [
                    "BEGIN:VEVENT",
                    "UID:{}".format(ics_escape(uid)),
                    "DTSTART;TZID={}:{}T{}".format(timezone, date_value, start),
                    "DTEND;TZID={}:{}T{}".format(timezone, date_value, end),
                    "SUMMARY:{}".format(ics_escape(item.get("name", "行程"))),
                    "DESCRIPTION:{}".format(ics_escape(item.get("description", ""))),
                    "END:VEVENT",
                ]
            )
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


def geojson_data(guide):
    features = []
    for day in guide.get("days", []):
        for item in day.get("items", []):
            coords = item.get("coords")
            if not coords or len(coords) != 2:
                continue
            features.append(
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": coords},
                    "properties": {
                        "name": item.get("name", ""),
                        "day": day.get("day"),
                        "date": day.get("date"),
                        "start": item.get("start"),
                        "end": item.get("end"),
                        "type": item.get("type", "spot"),
                    },
                }
            )
    return {"type": "FeatureCollection", "features": features}


def export_all(guide, output_base):
    base = Path(output_base)
    base.parent.mkdir(parents=True, exist_ok=True)
    markdown_path = base.with_suffix(".md")
    calendar_path = base.with_suffix(".ics")
    geojson_path = base.with_suffix(".geojson")
    markdown_path.write_text(markdown_text(guide), encoding="utf-8")
    with calendar_path.open("w", encoding="utf-8", newline="") as calendar_file:
        calendar_file.write(ics_text(guide))
    write_json(geojson_path, geojson_data(guide))
    return [str(markdown_path), str(calendar_path), str(geojson_path)]


def main():
    parser = argparse.ArgumentParser(description="导出旅游攻略")
    parser.add_argument("input", help="攻略 JSON 文件")
    parser.add_argument("--output-base", help="输出基础路径（不含扩展名）")
    args = parser.parse_args()
    guide = load_json(args.input)
    output_base = args.output_base or str(Path(args.input).with_suffix(""))
    print(
        json.dumps(
            {"status": "ok", "files": export_all(guide, output_base)},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
