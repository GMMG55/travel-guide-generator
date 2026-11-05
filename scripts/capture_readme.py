#!/usr/bin/env python3
"""Capture complete guide sections for README (requires Playwright + a browser)."""

import argparse
import math
from pathlib import Path

from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--channel", default="msedge", help="Installed browser channel")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    target = root / "assets" / "screenshots"
    target.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, channel=args.channel)
        context = browser.new_context(viewport={"width": 1120, "height": 1000}, device_scale_factor=2)
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto((root / "examples" / "qingdao-couple.html").as_uri())
        page.wait_for_load_state("networkidle")
        first_day = page.locator(".day-card").first
        bounds = first_day.bounding_box()
        overview_height = math.ceil(bounds["y"] + bounds["height"] + 24)
        page.set_viewport_size({"width": 1120, "height": overview_height})
        page.screenshot(path=str(target / "qingdao-overview.png"))
        page.set_viewport_size({"width": 1120, "height": 1000})
        first_day.screenshot(path=str(target / "qingdao-desktop.png"))
        page.screenshot(path=str(target / "qingdao-full.png"), full_page=True)
        lunch = first_day.locator(".itinerary-item").nth(1)
        assert not lunch.locator(".cost-input").is_visible()
        lunch.locator(".edit-btn").click()
        assert lunch.locator(".cost-input").is_visible()
        lunch.locator(".spot-desc").click()
        lunch.screenshot(path=str(target / "qingdao-edit.png"))
        lunch.locator(".edit-btn").click()
        page.locator(".budget-card").screenshot(path=str(target / "qingdao-budget.png"))
        page.set_viewport_size({"width": 390, "height": 844})
        first_day.screenshot(path=str(target / "qingdao-mobile.png"))
        for width in (375, 390, 768, 1440):
            page.set_viewport_size({"width": width, "height": 1000})
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), width
        assert not errors, errors
        browser.close()
    print("Captured full sections at 2x resolution; editing and responsive checks passed.")


if __name__ == "__main__":
    main()
