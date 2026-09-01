#!/usr/bin/env python3
"""Offline route-distance and duration estimation."""

import argparse
import json
import math


MODE_SPEED_KMH = {
    "walk": 4.5,
    "bike": 15.0,
    "transit": 22.0,
    "drive": 30.0,
}

MODE_FACTORS = {
    "walk": 1.15,
    "bike": 1.2,
    "transit": 1.35,
    "drive": 1.3,
}


def haversine_km(origin, destination):
    """Calculate great-circle distance between [lng, lat] pairs."""
    origin_lng, origin_lat = (float(value) for value in origin)
    destination_lng, destination_lat = (float(value) for value in destination)
    radius_km = 6371.0088
    lat1 = math.radians(origin_lat)
    lat2 = math.radians(destination_lat)
    delta_lat = lat2 - lat1
    delta_lng = math.radians(destination_lng - origin_lng)
    value = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lng / 2) ** 2
    )
    return radius_km * 2 * math.asin(math.sqrt(value))


def estimate_route(origin, destination, mode="drive", area="urban"):
    """Estimate route distance and duration without a map API."""
    if mode not in MODE_SPEED_KMH:
        raise ValueError("unsupported mode: {}".format(mode))
    straight_km = haversine_km(origin, destination)
    factor = MODE_FACTORS[mode]
    distance_km = straight_km * factor
    speed_kmh = MODE_SPEED_KMH[mode]
    if mode == "drive" and area == "intercity":
        speed_kmh = 60.0
    duration_min = max(1, round(distance_km / speed_kmh * 60))
    return {
        "mode": mode,
        "distance_km": round(distance_km, 1),
        "duration_min": duration_min,
        "estimated": True,
        "method": "haversine_x_{:.2f}".format(factor),
    }


def parse_coordinate(value):
    """Parse lng,lat CLI coordinates."""
    coordinate = [float(item.strip()) for item in value.split(",")]
    if len(coordinate) != 2:
        raise ValueError("coordinate must use lng,lat format")
    return coordinate


def main():
    parser = argparse.ArgumentParser(description="离线路线距离与用时估算")
    parser.add_argument("--origin", required=True, help="起点坐标 lng,lat")
    parser.add_argument("--destination", required=True, help="终点坐标 lng,lat")
    parser.add_argument(
        "--mode",
        choices=sorted(MODE_SPEED_KMH),
        default="drive",
        help="交通方式",
    )
    parser.add_argument(
        "--area", choices=["urban", "intercity"], default="urban"
    )
    args = parser.parse_args()
    try:
        result = estimate_route(
            parse_coordinate(args.origin),
            parse_coordinate(args.destination),
            args.mode,
            args.area,
        )
        result["status"] = "ok"
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (TypeError, ValueError) as error:
        print(
            json.dumps(
                {"status": "error", "message": str(error), "fallback": True},
                ensure_ascii=False,
            )
        )


if __name__ == "__main__":
    main()
