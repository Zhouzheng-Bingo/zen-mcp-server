#!/usr/bin/env python3
"""Direct API test for Zen models"""

import requests
import json

def test_yunwu_models():
    """Test models via YunWu API directly"""
    
    # Read custom models config
    with open('custom_models.json', 'r') as f:
        config = json.load(f)
    
    providers = {p['name']: p for p in config['providers']}
    
    # Test O3 model
    print("=== Testing O3 Model ===")
    o3_provider = providers['yunwu-o3']
    headers = {
        'Authorization': f'Bearer {o3_provider["api_key"]}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'o3',
        'messages': [{'role': 'user', 'content': '请用一句话解释什么是递归'}],
        'temperature': 0.7
    }
    
    try:
        response = requests.post(
            f'{o3_provider["api_url"]}/chat/completions',
            headers=headers,
            json=data
        )
        result = response.json()
        if 'choices' in result:
            print(f"O3 Response: {result['choices'][0]['message']['content']}")
        else:
            print(f"O3 Error: {result}")
    except Exception as e:
        print(f"O3 Exception: {e}")
    
    # Test Gemini Flash
    print("\n=== Testing Gemini Flash ===")
    gemini_provider = providers['yunwu-gemini']
    headers = {
        'Authorization': f'Bearer {gemini_provider["api_key"]}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'gemini-2.5-flash',
        'messages': [{'role': 'user', 'content': 'What is 2+2?'}],
        'temperature': 0.7
    }
    
    try:
        response = requests.post(
            f'{gemini_provider["api_url"]}/chat/completions',
            headers=headers,
            json=data
        )
        result = response.json()
        if 'choices' in result:
            print(f"Gemini Flash Response: {result['choices'][0]['message']['content']}")
        else:
            print(f"Gemini Flash Error: {result}")
    except Exception as e:
        print(f"Gemini Flash Exception: {e}")

if __name__ == "__main__":
    test_yunwu_models()