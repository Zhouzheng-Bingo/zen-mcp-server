#!/bin/bash

# copy_zen_to_project.sh - 将Zen AI模型集成复制到目标项目
# 用法: ./copy_zen_to_project.sh <目标项目路径>

set -e

if [ $# -eq 0 ]; then
    echo "错误: 请提供目标项目路径"
    echo "用法: $0 <目标项目路径>"
    exit 1
fi

TARGET_DIR="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📋 开始复制Zen AI文件到项目..."
echo "   源目录: $SCRIPT_DIR"
echo "   目标目录: $TARGET_DIR"

# 检查目标目录是否存在
if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ 错误: 目标目录不存在: $TARGET_DIR"
    exit 1
fi

# 创建zen_tools目录
mkdir -p "$TARGET_DIR/zen_tools"

# 复制配置文件
echo "📁 复制配置文件..."
cp "$SCRIPT_DIR/custom_models.json" "$TARGET_DIR/zen_tools/"

# 复制.env文件（包含API密钥）
if [ -f "$SCRIPT_DIR/.env" ]; then
    echo "🔑 复制.env文件..."
    cp "$SCRIPT_DIR/.env" "$TARGET_DIR/zen_tools/"
else
    echo "⚠️  警告: .env文件不存在，你可能需要手动创建并添加API密钥"
fi

# 创建简化的zen_ai.py接口
echo "🐍 创建zen_ai.py接口..."
cat > "$TARGET_DIR/zen_ai.py" << 'EOF'
#!/usr/bin/env python3
"""
Zen AI - 简化的多模型AI接口
提供对O3和Gemini模型的直接访问
"""

import json
import requests
import os
from pathlib import Path
from typing import Optional, Dict, Any, List

class ZenAI:
    def __init__(self):
        self.config_path = Path(__file__).parent / "zen_tools" / "custom_models.json"
        self.providers = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """加载模型配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return {p['name']: p for p in config['providers']}
        except Exception as e:
            print(f"❌ 配置加载失败: {e}")
            return {}
    
    def models(self) -> List[str]:
        """列出所有可用模型"""
        available_models = []
        for provider_name, provider in self.providers.items():
            for model in provider['models']:
                available_models.append(model['id'])
                print(f"🤖 {model['id']} - {model['name']}")
                print(f"   📝 {model['description']}")
                print(f"   🔢 上下文: {model['context_window']:,} tokens")
                print()
        return available_models
    
    def _find_model_provider(self, model_id: str) -> Optional[Dict[str, Any]]:
        """查找模型对应的提供商"""
        for provider in self.providers.values():
            for model in provider['models']:
                if model['id'] == model_id:
                    return provider
        return None
    
    def chat(self, prompt: str, model: str = 'gemini-2.5-flash') -> str:
        """与指定模型对话"""
        provider = self._find_model_provider(model)
        if not provider:
            return f"❌ 模型 {model} 不可用"
        
        try:
            headers = {
                'Authorization': f"Bearer {provider['api_key']}",
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': model,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'max_tokens': 4000,
                'temperature': 0.7
            }
            
            response = requests.post(
                f"{provider['api_url']}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"❌ API调用失败: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"❌ 请求失败: {str(e)}"

# 便捷函数
def ask_gemini(prompt: str, model: str = 'gemini-2.5-flash') -> str:
    """使用Gemini模型快速问答"""
    ai = ZenAI()
    return ai.chat(prompt, model)

def ask_o3(prompt: str, model: str = 'o3-mini') -> str:
    """使用O3模型进行推理"""
    ai = ZenAI()
    return ai.chat(prompt, model)

def list_models() -> List[str]:
    """列出可用模型"""
    ai = ZenAI()
    return ai.models()

# 主程序 - 显示可用模型
if __name__ == "__main__":
    print("🚀 Zen AI 模型系统")
    print("=" * 50)
    
    ai = ZenAI()
    if not ai.providers:
        print("❌ 没有找到可用的模型配置")
        print("   请确保 zen_tools/custom_models.json 文件存在")
        exit(1)
    
    print("📋 可用模型:")
    models = ai.models()
    
    print(f"✅ 共找到 {len(models)} 个模型")
    print("\n💡 使用示例:")
    print("from zen_ai import ask_gemini, ask_o3")
    print("answer = ask_gemini('什么是机器学习?')")
    print("solution = ask_o3('设计一个排序算法')")
EOF

# 创建使用示例
echo "📄 创建使用示例..."
cat > "$TARGET_DIR/zen_ai_example.py" << 'EOF'
#!/usr/bin/env python3
"""
Zen AI 使用示例 - 展示如何在G-code项目中使用AI模型
"""

from zen_ai import ZenAI, ask_gemini, ask_o3

def basic_usage():
    """基本用法示例"""
    print("=== 基本用法 ===")
    
    # 快速问答
    answer = ask_gemini("什么是CNC编程?")
    print(f"Gemini回答: {answer[:200]}...")
    
    # 复杂推理
    solution = ask_o3("设计一个G代码优化思路")
    print(f"O3方案: {solution[:200]}...")

def advanced_usage():
    """高级用法示例"""
    print("\n=== 高级用法 ===")
    
    ai = ZenAI()
    
    # 使用特定模型
    response = ai.chat(
        "分析以下G代码的性能: G01 X10 Y20 F100", 
        model='gemini-2.5-pro'
    )
    print(f"深度分析: {response[:200]}...")
    
    # 对比不同模型
    models_to_test = ['gemini-2.5-flash', 'o3-mini']
    question = "什么是数控加工?"
    
    for model in models_to_test:
        response = ai.chat(question, model)
        print(f"\n{model} 回答:")
        print(response[:150] + "...")

if __name__ == "__main__":
    # 首先列出可用模型
    print("🔍 检查可用模型...")
    from zen_ai import list_models
    models = list_models()
    
    if models:
        print(f"\n✅ 发现 {len(models)} 个模型，开始测试...")
        basic_usage()
        advanced_usage()
    else:
        print("❌ 没有可用模型，请检查配置")
EOF

# 创建requirements.txt（如果不存在）
if [ ! -f "$TARGET_DIR/requirements.txt" ]; then
    echo "📦 创建requirements.txt..."
    cat > "$TARGET_DIR/requirements.txt" << 'EOF'
requests>=2.28.0
EOF
else
    # 检查是否已包含requests
    if ! grep -q "requests" "$TARGET_DIR/requirements.txt"; then
        echo "requests>=2.28.0" >> "$TARGET_DIR/requirements.txt"
        echo "📦 添加requests依赖到现有requirements.txt"
    fi
fi

# 设置执行权限
chmod +x "$TARGET_DIR/zen_ai.py"
chmod +x "$TARGET_DIR/zen_ai_example.py"

echo ""
echo "✅ 复制完成！"
echo ""
echo "📋 已创建的文件:"
echo "   📄 $TARGET_DIR/zen_ai.py - 主要AI接口"
echo "   📄 $TARGET_DIR/zen_ai_example.py - 使用示例"
echo "   📁 $TARGET_DIR/zen_tools/custom_models.json - 模型配置
   📁 $TARGET_DIR/zen_tools/.env - API密钥配置"
echo ""
echo "🔬 测试安装:"
echo "   cd \"$TARGET_DIR\""
echo "   python zen_ai.py"
echo ""
echo "💡 日常使用:"
echo "   from zen_ai import ask_gemini, ask_o3"
echo "   answer = ask_gemini('你的问题')"
echo ""
echo "🎉 集成完成！可以在G-code项目中使用Zen AI了！"