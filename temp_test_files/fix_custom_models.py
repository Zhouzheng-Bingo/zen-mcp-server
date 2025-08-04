#!/usr/bin/env python3
"""
修复Zen MCP Server以支持custom_models.json中的模型
"""

import json
import os
import shutil

def fix_custom_models():
    """确保custom_models.json被正确加载"""
    
    print("修复Zen MCP Server模型配置...")
    
    # 1. 确保conf目录存在并复制配置文件
    os.makedirs('conf', exist_ok=True)
    if os.path.exists('custom_models.json'):
        shutil.copy2('custom_models.json', 'conf/custom_models.json')
        print("✓ 已复制custom_models.json到conf目录")
    
    # 2. 创建一个包装脚本来强制使用自定义模型
    wrapper_script = '''#!/usr/bin/env python3
"""
Zen MCP Server包装器 - 强制使用custom_models.json中的模型
"""

import os
import sys
import json

# 设置环境变量以使用自定义模型
def setup_custom_models():
    # 读取custom_models.json
    config_path = os.path.join(os.path.dirname(__file__), 'custom_models.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # 使用第一个provider的配置
        if config.get('providers') and len(config['providers']) > 0:
            provider = config['providers'][0]
            os.environ['CUSTOM_API_URL'] = provider['api_url']
            os.environ['CUSTOM_API_KEY'] = provider['api_key']
            
            # 设置默认模型为o3-mini（更快响应）
            os.environ['CUSTOM_MODEL_NAME'] = 'o3-mini'
            
            print(f"已配置使用: {provider['name']}")
            print(f"API URL: {provider['api_url']}")
            print(f"默认模型: o3-mini")

# 在导入server之前设置环境变量
setup_custom_models()

# 导入并运行原始server
sys.path.insert(0, os.path.dirname(__file__))
from server import main

if __name__ == "__main__":
    main()
'''
    
    with open('zen_server_wrapper.py', 'w') as f:
        f.write(wrapper_script)
    os.chmod('zen_server_wrapper.py', 0o755)
    print("✓ 创建了zen_server_wrapper.py包装脚本")
    
    # 3. 更新.mcp.json以使用包装脚本
    mcp_config = {
        "mcpServers": {
            "zen": {
                "command": "python",
                "args": [f"{os.getcwd()}/zen_server_wrapper.py"],
                "env": {
                    "PYTHONPATH": os.getcwd()
                }
            }
        }
    }
    
    with open('.mcp.json', 'w') as f:
        json.dump(mcp_config, f, indent=2)
    print("✓ 更新了.mcp.json配置")
    
    # 4. 创建一个测试脚本
    test_script = '''#!/usr/bin/env python3
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
    print("\\n测试Gemini模型...")
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
'''
    
    with open('test_custom_models.py', 'w') as f:
        f.write(test_script)
    os.chmod('test_custom_models.py', 0o755)
    print("✓ 创建了test_custom_models.py测试脚本")
    
    print("\n完成！请执行以下步骤：")
    print("1. 重启Claude Code")
    print("2. 现在您可以在对话中使用Zen工具了，例如：")
    print("   - '使用Gemini分析这段代码'")
    print("   - '用O3深入思考这个问题'")
    print("   - '让多个模型协作解决这个问题'")

if __name__ == "__main__":
    fix_custom_models()