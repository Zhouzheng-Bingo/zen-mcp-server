#!/usr/bin/env python3
"""Test Zen MCP models functionality"""

import asyncio
import json
from pathlib import Path
from tools.chat import ChatTool

async def test_models():
    """Test different models via Zen MCP"""
    chat_tool = ChatTool()
    
    # Test 1: List available models
    print("=== Testing Model Listing ===")
    try:
        result = await chat_tool.handle_tool_call(
            name="listmodels",
            arguments={"model": "local"}
        )
        print(f"Available models response: {result.get('content', 'No content')[:500]}...")
    except Exception as e:
        print(f"Error listing models: {e}")
    
    # Test 2: Chat with O3 model
    print("\n=== Testing O3 Model ===")
    try:
        result = await chat_tool.handle_tool_call(
            name="chat",
            arguments={
                "prompt": "请用一句话解释什么是递归",
                "model": "o3"
            }
        )
        print(f"O3 response: {result.get('content', 'No content')}")
    except Exception as e:
        print(f"Error with O3: {e}")
    
    # Test 3: Chat with Gemini Flash
    print("\n=== Testing Gemini Flash ===")
    try:
        result = await chat_tool.handle_tool_call(
            name="chat",
            arguments={
                "prompt": "What is 2+2?",
                "model": "gemini-2.5-flash"
            }
        )
        print(f"Gemini Flash response: {result.get('content', 'No content')}")
    except Exception as e:
        print(f"Error with Gemini Flash: {e}")
    
    # Test 4: Deep thinking with Gemini Pro
    print("\n=== Testing Gemini Pro Deep Thinking ===")
    try:
        from tools.thinkdeep import ThinkDeepTool
        thinkdeep_tool = ThinkDeepTool()
        result = await thinkdeep_tool.handle_tool_call(
            name="thinkdeep",
            arguments={
                "prompt": "分析Python异步编程的优缺点",
                "model": "gemini-2.5-pro"
            }
        )
        print(f"Gemini Pro deep thinking: {result.get('content', 'No content')[:500]}...")
    except Exception as e:
        print(f"Error with Gemini Pro: {e}")

if __name__ == "__main__":
    asyncio.run(test_models())