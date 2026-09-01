#!/usr/bin/env python3
"""Validate structured travel guides and detect itinerary conflicts."""

import argparse
import json
from datetime import date

try:
    from .guide_utils import checked_age_days, load_json, parse_hhmm, parse_iso_date
except ImportError:
    from guide_utils import checked_age_days, load_json, parse_hhmm, parse_iso_date


REQUIRED_META_FIELDS = ("title", "destination", "language", "start_date", "days")
VALID_PACES = {"relaxed", "balanced", "intensive"}
VALID_SOURCE_TYPES = {"official", "search", "user", "estimate", "general"}


def issue(level, code, message, path):
    """Create a consistent validation issue."""
    return {"level": level, "code": code, "message": message, "path": path}


def validate_sources(guide, errors, warnings, today):
    source_ids = set()
    for index, source in enumerate(guide.get("sources", [])):
        path = "sources[{}]".format(index)
        source_id = source.get("id")
        if not source_id:
            errors.append(issue("error", "SOURCE_ID", "来源缺少 id", path))
        elif source_id in source_ids:
            errors.append(issue("error", "SOURCE_DUPLICATE", "来源 id 重复", path))
        else:
            source_ids.add(source_id)
        source_type = source.get("type", "search")
        if source_type not in VALID_SOURCE_TYPES:
            warnings.append(issue("warning", "SOURCE_TYPE", "未知来源类型", path))
        url = source.get("url")
        if url and not str(url).startswith(("https://", "http://")):
            errors.append(issue("error", "SOURCE_URL", "来源 URL 必须使用 HTTP(S)", path))
        age = checked_age_days(source.get("checked_at"), today)
        if source.get("checked_at") and age is None:
            errors.append(issue("error", "SOURCE_DATE", "核实日期格式应为 YYYY-MM-DD", path))
        elif age is not None and age > 180:
            warnings.append(
                issue("warning", "SOURCE_STALE", "来源已超过 180 天，建议重新核实", path)
            )
    return source_ids


def validate_source_refs(record, path, source_ids, warnings):
    refs = record.get("source_ids", [])
    for source_id in refs:
        if source_id not in source_ids:
            warnings.append(
                issue(
                    "warning",
                    "SOURCE_MISSING",
                    "引用了不存在的来源 {}".format(source_id),
                    path,
                )
            )


def validate_days(guide, source_ids, errors, warnings, conflicts):
    days = guide.get("days", [])
    expected_days = guide.get("meta", {}).get("days")
    if isinstance(expected_days, int) and expected_days != len(days):
        errors.append(
            issue(
                "error",
                "DAY_COUNT",
                "meta.days 与实际 days 数量不一致",
                "days",
            )
        )
    for day_index, day in enumerate(days):
        day_path = "days[{}]".format(day_index)
        try:
            day_date = parse_iso_date(day.get("date"))
        except (TypeError, ValueError):
            errors.append(issue("error", "DAY_DATE", "日期格式应为 YYYY-MM-DD", day_path))
            day_date = None
        items = day.get("items", [])
        if not items:
            errors.append(issue("error", "DAY_EMPTY", "每天至少需要一个行程项", day_path))
            continue
        previous_end = None
        previous_name = None
        for item_index, item in enumerate(items):
            path = "{}.items[{}]".format(day_path, item_index)
            if not item.get("name"):
                errors.append(issue("error", "ITEM_NAME", "行程项缺少名称", path))
            validate_source_refs(item, path, source_ids, warnings)
            try:
                start = parse_hhmm(item.get("start"))
                end = parse_hhmm(item.get("end"))
            except (TypeError, ValueError, AttributeError):
                errors.append(issue("error", "ITEM_TIME", "时间格式应为 HH:MM", path))
                continue
            if end <= start:
                errors.append(issue("error", "ITEM_RANGE", "结束时间必须晚于开始时间", path))
            if previous_end is not None and start < previous_end:
                conflicts.append(
                    issue(
                        "conflict",
                        "TIME_OVERLAP",
                        "{} 与 {} 时间重叠".format(previous_name, item.get("name", "未命名项")),
                        path,
                    )
                )
            route = item.get("route_from_previous") or {}
            if previous_end is not None and route.get("duration_min") is not None:
                available = start - previous_end
                if int(route["duration_min"]) > available:
                    conflicts.append(
                        issue(
                            "conflict",
                            "TRANSIT_TOO_SHORT",
                            "预留 {} 分钟，但交通需要约 {} 分钟".format(
                                available, route["duration_min"]
                            ),
                            path,
                        )
                    )
                if route.get("estimated") and not route.get("method"):
                    warnings.append(
                        issue("warning", "ESTIMATE_METHOD", "估算路线缺少估算方法", path)
                    )
            opening = item.get("opening_hours") or {}
            if opening:
                try:
                    opening_min = parse_hhmm(opening.get("open"))
                    closing_min = parse_hhmm(opening.get("close"))
                    if start < opening_min or end > closing_min:
                        conflicts.append(
                            issue(
                                "conflict",
                                "OUTSIDE_OPENING_HOURS",
                                "行程超出开放时间 {}-{}".format(
                                    opening.get("open"), opening.get("close")
                                ),
                                path,
                            )
                        )
                except (TypeError, ValueError, AttributeError):
                    warnings.append(
                        issue("warning", "OPENING_HOURS", "开放时间格式无效", path)
                    )
            if day_date and day_date.strftime("%a").lower() in {
                str(value).lower() for value in item.get("closed_weekdays", [])
            }:
                conflicts.append(
                    issue("conflict", "CLOSED_DAY", "该地点在行程当天可能闭馆", path)
                )
            previous_end = max(previous_end or 0, end)
            previous_name = item.get("name", "未命名项")


def validate_preferences(guide, errors, warnings):
    preferences = guide.get("preferences", {})
    pace = preferences.get("pace")
    if pace and pace not in VALID_PACES:
        warnings.append(issue("warning", "PACE", "未知行程节奏", "preferences.pace"))
    earliest = preferences.get("earliest_start")
    latest = preferences.get("latest_end")
    if earliest and latest:
        try:
            earliest_min = parse_hhmm(earliest)
            latest_min = parse_hhmm(latest)
            for day_index, day in enumerate(guide.get("days", [])):
                for item_index, item in enumerate(day.get("items", [])):
                    try:
                        start = parse_hhmm(item.get("start"))
                        end = parse_hhmm(item.get("end"))
                    except (TypeError, ValueError, AttributeError):
                        continue
                    path = "days[{}].items[{}]".format(day_index, item_index)
                    if start < earliest_min:
                        warnings.append(
                            issue("warning", "TOO_EARLY", "早于用户偏好的出发时间", path)
                        )
                    if end > latest_min:
                        warnings.append(
                            issue("warning", "TOO_LATE", "晚于用户偏好的结束时间", path)
                        )
        except (TypeError, ValueError, AttributeError):
            errors.append(
                issue("error", "PREFERENCE_TIME", "偏好时间格式应为 HH:MM", "preferences")
            )


def validate_guide(guide, today=None):
    """Validate guide structure and return errors, warnings and conflicts."""
    errors = []
    warnings = []
    conflicts = []
    if not isinstance(guide, dict):
        return {
            "valid": False,
            "errors": [issue("error", "ROOT", "攻略根节点必须是对象", "$")],
            "warnings": [],
            "conflicts": [],
        }
    if guide.get("schema_version") != "1.0":
        errors.append(
            issue("error", "SCHEMA_VERSION", "schema_version 必须为 1.0", "schema_version")
        )
    meta = guide.get("meta")
    if not isinstance(meta, dict):
        errors.append(issue("error", "META", "缺少 meta 对象", "meta"))
        meta = {}
    for field in REQUIRED_META_FIELDS:
        if meta.get(field) in (None, ""):
            errors.append(
                issue("error", "META_FIELD", "缺少字段 {}".format(field), "meta.{}".format(field))
            )
    try:
        parse_iso_date(meta.get("start_date"))
    except (TypeError, ValueError):
        errors.append(
            issue("error", "START_DATE", "开始日期格式应为 YYYY-MM-DD", "meta.start_date")
        )
    if not isinstance(guide.get("days"), list):
        errors.append(issue("error", "DAYS", "days 必须是数组", "days"))
        guide = dict(guide)
        guide["days"] = []
    source_ids = validate_sources(guide, errors, warnings, today or date.today())
    validate_preferences(guide, errors, warnings)
    validate_days(guide, source_ids, errors, warnings, conflicts)
    for collection in ("transport", "hotels", "foods", "avoid"):
        for index, record in enumerate(guide.get(collection, [])):
            validate_source_refs(record, "{}[{}]".format(collection, index), source_ids, warnings)
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "conflicts": conflicts,
    }


def main():
    parser = argparse.ArgumentParser(description="校验结构化旅游攻略")
    parser.add_argument("input", help="攻略 JSON 文件")
    parser.add_argument("--strict", action="store_true", help="冲突或警告也返回非零状态")
    args = parser.parse_args()
    try:
        report = validate_guide(load_json(args.input))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        report = {
            "valid": False,
            "errors": [issue("error", "INPUT", str(error), "$")],
            "warnings": [],
            "conflicts": [],
        }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    failed = not report["valid"] or (
        args.strict and (report["warnings"] or report["conflicts"])
    )
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
