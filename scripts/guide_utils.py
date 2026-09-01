#!/usr/bin/env python3
"""Shared helpers for structured travel-guide scripts."""

import json
from datetime import date, datetime
from html import escape
from pathlib import Path


def load_json(path):
    """Load UTF-8 JSON from *path*."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, data):
    """Write deterministic, human-readable UTF-8 JSON."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def text(value):
    """Escape a value for safe insertion into HTML text or attributes."""
    return escape(str(value if value is not None else ""), quote=True)


def parse_hhmm(value):
    """Convert HH:MM text to minutes after midnight."""
    hour, minute = str(value).split(":", 1)
    hour = int(hour)
    minute = int(minute)
    if not 0 <= hour <= 23 or not 0 <= minute <= 59:
        raise ValueError("time must be between 00:00 and 23:59")
    return hour * 60 + minute


def format_hhmm(minutes):
    """Convert minutes after midnight to HH:MM, wrapping at 24 hours."""
    minutes = int(minutes) % (24 * 60)
    return "{:02d}:{:02d}".format(minutes // 60, minutes % 60)


def parse_iso_date(value):
    """Parse an ISO date on Python 3.8+."""
    return datetime.strptime(str(value), "%Y-%m-%d").date()


def checked_age_days(value, today=None):
    """Return source age in days, or None for an invalid/missing date."""
    if not value:
        return None
    try:
        checked = parse_iso_date(value)
    except (TypeError, ValueError):
        return None
    return ((today or date.today()) - checked).days


def source_index(guide):
    """Index source records by id."""
    return {
        source.get("id"): source
        for source in guide.get("sources", [])
        if source.get("id")
    }


def source_badges(source_ids, sources):
    """Render compact, escaped source links."""
    badges = []
    for source_id in source_ids or []:
        source = sources.get(source_id)
        if not source:
            continue
        label = source.get("title") or source_id
        url = source.get("url")
        checked_at = source.get("checked_at")
        suffix = " · {}".format(checked_at) if checked_at else ""
        if url and str(url).startswith(("https://", "http://")):
            badges.append(
                '<a class="source-badge" href="{}" target="_blank" '
                'rel="noopener noreferrer">{}{}{}</a>'.format(
                    text(url),
                    text(label),
                    text(suffix),
                    "",
                )
            )
        else:
            badges.append(
                '<span class="source-badge">{}{}</span>'.format(
                    text(label), text(suffix)
                )
            )
    return "".join(badges)


def json_for_script(data):
    """Serialize JSON safely for embedding in a script element."""
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
