#!/usr/bin/env python3
"""
旅游攻略搜索脚本
搜索小红书、马蜂窝等平台的攻略内容
"""

import argparse
import json
import sys

def format_search_queries(destination, query_type="general"):
    """
    根据目的地和查询类型生成搜索关键词
    
    Args:
        destination: 目的地名称
        query_type: 查询类型 (general/food/avoid/hotel/transport)
    
    Returns:
        搜索关键词列表
    """
    
    queries = {
        "general": [
            f"{destination}旅游攻略",
            f"{destination}必去景点",
            f"{destination}行程安排",
            f"{destination}自由行攻略"
        ],
        "food": [
            f"{destination}美食推荐",
            f"{destination}必吃美食",
            f"{destination}网红餐厅",
            f"{destination}本地人推荐美食"
        ],
        "avoid": [
            f"{destination}避坑指南",
            f"{destination}旅游陷阱",
            f"{destination}注意事项",
            f"{destination}踩雷"
        ],
        "hotel": [
            f"{destination}酒店推荐",
            f"{destination}住宿攻略",
            f"{destination}民宿推荐",
            f"{destination}住哪里方便"
        ],
        "transport": [
            f"{destination}怎么去",
            f"{destination}交通攻略",
            f"{destination}机场到市区",
            f"{destination}高铁站"
        ],
        "romantic": [
            f"{destination}情侣打卡",
            f"{destination}浪漫景点",
            f"{destination}约会地点",
            f"{destination}拍照好看"
        ]
    }
    
    return queries.get(query_type, queries["general"])

def main():
    parser = argparse.ArgumentParser(description="旅游攻略搜索关键词生成")
    parser.add_argument("--destination", required=True, help="目的地名称")
    parser.add_argument("--type", default="general", 
                       choices=["general", "food", "avoid", "hotel", "transport", "romantic"],
                       help="查询类型")
    parser.add_argument("--all", action="store_true", help="生成所有类型的搜索词")
    
    args = parser.parse_args()
    
    if args.all:
        # 生成所有类型的搜索词
        all_queries = {}
        for query_type in ["general", "food", "avoid", "hotel", "transport", "romantic"]:
            all_queries[query_type] = format_search_queries(args.destination, query_type)
        
        result = {
            "destination": args.destination,
            "search_queries": all_queries,
            "usage": "使用这些关键词在在线搜索工具中搜索，获取真实攻略内容"
        }
    else:
        queries = format_search_queries(args.destination, args.type)
        result = {
            "destination": args.destination,
            "type": args.type,
            "search_queries": queries,
            "usage": "使用这些关键词在在线搜索工具中搜索，获取真实攻略内容"
        }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
