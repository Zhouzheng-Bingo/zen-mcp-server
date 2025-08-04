#!/usr/bin/env python3
"""测试自定义模型是否工作"""

import asyncio
from tools.chat import ChatTool

async def test():
    chat = ChatTool()
    
    # 测试O3模型
    print("测试O3模型...")
    try:
        result = await chat.run(
            prompt="简单解释什么是递归",
            model="o3-mini"
        )
        print(f"O3回答: {result.content[:200]}...")
    except Exception as e:
        print(f"O3错误: {e}")
    
    # 测试Gemini模型
    print("\n测试Gemini模型...")
    try:
        # 需要切换到gemini provider
        import os
        provider = next(p for p in config['providers'] if 'gemini' in p['name'])
        os.environ['CUSTOM_API_KEY'] = provider['api_key']
        
        result = await chat.run(
            prompt="What is 2+2?",
            model="gemini-2.5-flash"
        )
        print(f"Gemini回答: {result.content}")
    except Exception as e:
        print(f"Gemini错误: {e}")

if __name__ == "__main__":
    with open('custom_models.json', 'r') as f:
        config = json.load(f)
    asyncio.run(test())
