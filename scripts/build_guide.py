#!/usr/bin/env python3
"""End-to-end structured travel-guide build pipeline."""

import argparse
import copy
import json
from pathlib import Path

try:
    from .export_guide import export_all
    from .guide_utils import load_json, write_json
    from .render_guide import render_file
    from .route_estimator import estimate_route
    from .season_advisor import build_season_tips
    from .validate_guide import validate_guide
except ImportError:
    from export_guide import export_all
    from guide_utils import load_json, write_json
    from render_guide import render_file
    from route_estimator import estimate_route
    from season_advisor import build_season_tips
    from validate_guide import validate_guide


def enrich_routes(guide):
    """Fill missing inter-item routes when both coordinates are available."""
    count = 0
    preferred_modes = guide.get("preferences", {}).get("transport", [])
    default_mode = preferred_modes[0] if preferred_modes else "drive"
    if default_mode not in {"walk", "bike", "transit", "drive"}:
        default_mode = "drive"
    for day in guide.get("days", []):
        previous = None
        for item in day.get("items", []):
            if previous and not item.get("route_from_previous"):
                origin = previous.get("coords")
                destination = item.get("coords")
                if origin and destination:
                    item["route_from_previous"] = estimate_route(
                        origin, destination, item.get("transport_mode", default_mode)
                    )
                    count += 1
            previous = item
    return count


def build(guide, output_base, template=None, allow_invalid=False):
    """Enrich, validate, render and export a guide."""
    enriched = copy.deepcopy(guide)
    route_count = enrich_routes(enriched)
    enriched["season_tips"] = build_season_tips(enriched)
    report = validate_guide(enriched)
    if not report["valid"] and not allow_invalid:
        return {
            "status": "error",
            "message": "攻略校验失败",
            "report": report,
            "files": [],
        }
    base = Path(output_base)
    normalized_path = base.with_suffix(".normalized.json")
    html_path = base.with_suffix(".html")
    write_json(normalized_path, enriched)
    render_file(enriched, html_path, template, allow_invalid=allow_invalid)
    files = [str(normalized_path), str(html_path)] + export_all(enriched, base)
    return {
        "status": "ok",
        "routes_estimated": route_count,
        "report": report,
        "files": files,
    }


def main():
    parser = argparse.ArgumentParser(description="构建并导出结构化旅游攻略")
    parser.add_argument("input", help="攻略 JSON 文件")
    parser.add_argument("--output-base", help="输出基础路径（不含扩展名）")
    parser.add_argument("--template", help="自定义 HTML 模板")
    parser.add_argument("--allow-invalid", action="store_true")
    args = parser.parse_args()
    output_base = args.output_base or str(Path(args.input).with_suffix(""))
    try:
        result = build(
            load_json(args.input),
            output_base,
            args.template,
            args.allow_invalid,
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        result = {"status": "error", "message": str(error), "files": []}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "ok" else 1)


if __name__ == "__main__":
    main()
