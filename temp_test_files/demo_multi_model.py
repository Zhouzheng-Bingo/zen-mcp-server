#!/usr/bin/env python3
"""
演示Zen MCP Server多模型协作能力
展示如何在一个连贯的对话中使用不同模型处理不同任务
"""

import json
import requests
import time

def call_model(api_url, api_key, model, prompt, temperature=0.7):
    """调用模型API"""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': temperature
    }
    
    try:
        response = requests.post(
            f'{api_url}/chat/completions',
            headers=headers,
            json=data,
            timeout=60
        )
        result = response.json()
        if 'choices' in result:
            return result['choices'][0]['message']['content']
        else:
            return f"错误: {result}"
    except Exception as e:
        return f"异常: {e}"

def demonstrate_multi_model_collaboration():
    """演示多模型协作"""
    
    print("=== Zen MCP Server 多模型协作演示 ===\n")
    
    # 读取custom_models.json配置
    with open('custom_models.json', 'r') as f:
        config = json.load(f)
    
    # 提取provider信息
    providers = {p['name']: p for p in config['providers']}
    
    print("已配置的模型提供商：")
    for name, provider in providers.items():
        print(f"\n✓ {name}")
        for model in provider['models']:
            print(f"  - {model['id']}: {model['name']} ({model['description']})")
    
    print("\n" + "="*60 + "\n")
    
    # 场景1: 使用O3模型进行复杂推理
    print("【场景1】使用O3模型进行复杂算法推理")
    print("-" * 50)
    
    o3_provider = providers['yunwu-o3']
    prompt1 = """请分析以下算法问题并给出解答：

问题：给定一个整数数组nums和一个目标值target，请找出数组中和为target的两个数的下标。

要求：
1. 提供最优解法
2. 分析时间复杂度
3. 给出Python代码实现"""
    
    print("正在调用O3模型...")
    start_time = time.time()
    response = call_model(
        o3_provider['api_url'],
        o3_provider['api_key'],
        'o3-mini',  # 使用o3-mini以加快响应
        prompt1
    )
    elapsed = time.time() - start_time
    print(f"\nO3模型回答 (耗时: {elapsed:.2f}秒)：")
    print(response[:800] + "..." if len(response) > 800 else response)
    
    # 场景2: 使用Gemini Pro分析代码架构
    print("\n\n【场景2】使用Gemini Pro深度分析代码架构")
    print("-" * 50)
    
    gemini_provider = providers['yunwu-gemini']
    prompt2 = """请简要分析MVC架构的核心设计理念，包括：
1. Model、View、Controller各自的职责
2. 它们之间的交互关系
3. MVC架构的主要优势"""
    
    print("正在调用Gemini Pro模型...")
    start_time = time.time()
    response = call_model(
        gemini_provider['api_url'],
        gemini_provider['api_key'],
        'gemini-2.5-pro',
        prompt2
    )
    elapsed = time.time() - start_time
    print(f"\nGemini Pro回答 (耗时: {elapsed:.2f}秒)：")
    print(response[:1000] + "..." if len(response) > 1000 else response)
    
    # 场景3: 使用Gemini Flash快速处理简单查询
    print("\n\n【场景3】使用Gemini Flash快速回答编程问题")
    print("-" * 50)
    
    prompt3 = "Python中list和tuple的主要区别是什么？用2-3句话简要说明。"
    
    print("正在调用Gemini Flash模型...")
    start_time = time.time()
    response = call_model(
        gemini_provider['api_url'],
        gemini_provider['api_key'],
        'gemini-2.5-flash',
        prompt3,
        temperature=0.5
    )
    elapsed = time.time() - start_time
    print(f"\nGemini Flash回答 (耗时: {elapsed:.2f}秒)：")
    print(response)
    
    # 场景4: 跨模型协作
    print("\n\n【场景4】跨模型协作 - 设计高性能缓存系统")
    print("-" * 50)
    print("让不同模型负责不同方面：")
    
    # Step 1: O3设计核心算法
    print("\n1. O3-mini负责设计核心算法...")
    algo_prompt = "设计一个LRU缓存的核心数据结构，要求O(1)的读写性能，简要说明关键思路。"
    
    start_time = time.time()
    algo_response = call_model(
        o3_provider['api_url'],
        o3_provider['api_key'],
        'o3-mini',
        algo_prompt
    )
    elapsed = time.time() - start_time
    print(f"   算法设计完成 (耗时: {elapsed:.2f}秒)")
    
    # Step 2: Gemini Flash快速总结
    print("\n2. Gemini Flash负责总结实现要点...")
    summary_prompt = "列出实现高性能缓存系统的3个关键技术点"
    
    start_time = time.time()
    summary_response = call_model(
        gemini_provider['api_url'],
        gemini_provider['api_key'],
        'gemini-2.5-flash',
        summary_prompt,
        temperature=0.3
    )
    elapsed = time.time() - start_time
    print(f"   要点总结完成 (耗时: {elapsed:.2f}秒)")
    print(f"\n   关键技术点：\n{summary_response}")
    
    print("\n" + "="*60)
    print("\n演示总结：")
    print("✓ O3模型 - 适合复杂推理和算法设计")
    print("✓ Gemini Pro - 适合深度分析和架构设计")
    print("✓ Gemini Flash - 适合快速响应和简单任务")
    print("✓ 通过合理分配任务，可以充分发挥各模型优势")
    
    # 关于API keys的说明
    print("\n关于您的API配置：")
    print("您配置了两个云雾AI的API key，分别用于：")
    print("1. yunwu-o3: 访问O3和O3-mini模型")
    print("2. yunwu-gemini: 访问Gemini Pro和Flash模型")
    print("这样的配置可以让您同时使用不同系列的模型。")

if __name__ == "__main__":
    demonstrate_multi_model_collaboration()