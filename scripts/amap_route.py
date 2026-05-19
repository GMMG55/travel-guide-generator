#!/usr/bin/env python3
"""
高德地图路线规划脚本
计算两点间的驾车距离和用时
"""

import argparse
import requests
import json
import sys
import os

def get_amap_key():
    """获取高德API key"""
    key = os.environ.get('AMAP_KEY')
    if not key:
        print("错误: 未设置AMAP_KEY环境变量", file=sys.stderr)
        print("请设置: export AMAP_KEY=your_key (Linux/Mac)", file=sys.stderr)
        print("或设置: set AMAP_KEY=your_key (Windows)", file=sys.stderr)
        sys.exit(1)
    return key

def geocode(address, city=None, key=None):
    """地址转经纬度"""
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        "key": key,
        "address": address,
        "output": "json"
    }
    if city:
        params["city"] = city
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        
        if data.get("status") == "1" and data.get("geocodes"):
            location = data["geocodes"][0]["location"]
            lng, lat = location.split(",")
            return f"{lng},{lat}"
        else:
            return None
    except Exception as e:
        print(f"地理编码错误: {e}", file=sys.stderr)
        return None

def get_driving_route(origin, destination, key):
    """获取驾车路线规划"""
    url = "https://restapi.amap.com/v3/direction/driving"
    params = {
        "key": key,
        "origin": origin,
        "destination": destination,
        "output": "json",
        "strategy": 0  # 推荐策略
    }
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        
        if data.get("status") == "1" and data.get("route"):
            path = data["route"]["paths"][0]
            distance = int(path["distance"])  # 米
            duration = int(path["duration"])  # 秒
            
            # 格式化输出
            distance_km = distance / 1000
            duration_min = duration / 60
            
            if distance < 1000:
                distance_text = f"{distance}米"
            else:
                distance_text = f"{distance_km:.1f}公里"
            
            if duration_min < 60:
                duration_text = f"{int(duration_min)}分钟"
            else:
                hours = int(duration_min // 60)
                mins = int(duration_min % 60)
                duration_text = f"{hours}小时{mins}分钟"
            
            # 提取路线坐标（用于地图绘制）
            steps = path.get("steps", [])
            polyline_coords = []
            for step in steps:
                # 每个step有polyline字段，格式为"lng,lat;lng,lat;..."
                polyline = step.get("polyline", "")
                if polyline:
                    points = polyline.split(";")
                    for pt in points:
                        lng, lat = pt.split(",")
                        polyline_coords.append([float(lng), float(lat)])
            
            return {
                "distance": distance,
                "duration": duration,
                "distance_text": distance_text,
                "duration_text": duration_text,
                "distance_km": distance_km,
                "duration_min": duration_min,
                "polyline": polyline_coords  # 新增：路线坐标数组
            }
        else:
            return None
    except Exception as e:
        print(f"路线规划错误: {e}", file=sys.stderr)
        return None

def get_multi_point_route(locations, key):
    """获取多点路线坐标（用于地图轨迹绘制）
    
    Args:
        locations: 坐标数组，格式 ["lng,lat", "lng,lat", ...]
        key: 高德API key
    
    Returns:
        合并后的路线坐标数组 [[lng,lat], ...]
    """
    all_coords = []
    
    for i in range(len(locations) - 1):
        origin = locations[i]
        destination = locations[i + 1]
        
        result = get_driving_route(origin, destination, key)
        if result and "polyline" in result:
            all_coords.extend(result["polyline"])
        else:
            # 如果路线规划失败，直接添加起终点坐标
            orig_coords = [float(x) for x in origin.split(",")]
            dest_coords = [float(x) for x in destination.split(",")]
            all_coords.append(orig_coords)
            all_coords.append(dest_coords)
    
    return all_coords

def main():
    parser = argparse.ArgumentParser(description="高德地图路线规划")
    parser.add_argument("--origin", help="起点地址")
    parser.add_argument("--destination", help="终点地址")
    parser.add_argument("--city", help="城市名称（提高地理编码准确性）")
    parser.add_argument("--key", help="高德API key（不提供则从环境变量读取）")
    parser.add_argument("--multi-point", nargs="+", help="多点路线（输入多个地址，用空格分隔）")
    parser.add_argument("--output-polyline", action="store_true", help="输出路线坐标（用于地图绘制）")
    
    args = parser.parse_args()
    
    # 获取API key
    key = args.key or get_amap_key()
    
    # 多点路线模式
    if args.multi_point:
        if len(args.multi_point) < 2:
            print("错误: --multi-point 需要至少2个地址", file=sys.stderr)
            sys.exit(1)
        
        print(f"正在查询多点路线: {' -> '.join(args.multi_point)}", file=sys.stderr)
        
        # 地理编码所有点
        locations = []
        for addr in args.multi_point:
            coord = geocode(addr, args.city, key)
            if not coord:
                print(f"错误: 无法找到地址 '{addr}'", file=sys.stderr)
                sys.exit(1)
            locations.append(coord)
        
        # 获取多点路线坐标
        all_coords = get_multi_point_route(locations, key)
        
        print(json.dumps({"polyline": all_coords}, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # 单点路线模式（原有逻辑）
    if not args.origin or not args.destination:
        parser.print_help()
        sys.exit(1)
    
    # 地理编码
    print(f"正在查询: {args.origin} -> {args.destination}", file=sys.stderr)
    
    origin_coord = geocode(args.origin, args.city, key)
    if not origin_coord:
        print(f"错误: 无法找到起点 '{args.origin}'", file=sys.stderr)
        sys.exit(1)
    
    dest_coord = geocode(args.destination, args.city, key)
    if not dest_coord:
        print(f"错误: 无法找到终点 '{args.destination}'", file=sys.stderr)
        sys.exit(1)
    
    # 路线规划
    result = get_driving_route(origin_coord, dest_coord, key)
    
    if result:
        # 如果不要求输出polyline，则删除该字段
        if not args.output_polyline:
            result.pop("polyline", None)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("错误: 路线规划失败", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
