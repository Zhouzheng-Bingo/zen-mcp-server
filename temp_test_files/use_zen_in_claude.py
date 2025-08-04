#!/usr/bin/env python3
"""
在Claude Code中使用Zen多模型协作的示例
"""

import asyncio
import json
from pathlib import Path

# 导入Zen工具
from tools.thinkdeep import ThinkDeepTool
from tools.codereview import CodeReviewTool
from tools.chat import ChatTool
from tools.testgen import TestGenTool

async def performance_optimization_workflow(code_file: str):
    """
    执行您描述的工作流程：
    1. 深入研究代码
    2. 思考性能优化
    3. 与Gemini协作获取反馈
    4. 添加单元测试
    """
    
    print("=== 开始性能优化工作流程 ===\n")
    
    # Step 1: 使用ThinkDeep深入研究代码
    print("1. 使用O3模型深入分析代码...")
    thinkdeep = ThinkDeepTool()
    analysis_result = await thinkdeep.handle_request({
        "prompt": f"请深入分析{code_file}的代码结构，识别性能瓶颈和优化机会",
        "files": [code_file],
        "model": "o3"  # 使用O3进行深度推理
    })
    print(f"分析完成: {analysis_result.content[:500]}...\n")
    
    # Step 2: 使用Gemini Pro获取架构反馈
    print("2. 使用Gemini Pro获取架构优化建议...")
    chat = ChatTool()
    gemini_feedback = await chat.handle_request({
        "prompt": f"""基于以下分析结果，请提供架构层面的性能优化建议：
{analysis_result.content[:1000]}

请重点关注：
1. 算法复杂度优化
2. 数据结构选择
3. 缓存策略
4. 并发优化机会""",
        "model": "gemini-2.5-pro"
    })
    print(f"Gemini反馈: {gemini_feedback.content[:500]}...\n")
    
    # Step 3: 使用CodeReview工具进行代码审查
    print("3. 执行代码审查...")
    codereview = CodeReviewTool()
    review_result = await codereview.handle_request({
        "files": [code_file],
        "model": "gemini-2.5-flash"  # 使用Flash快速审查
    })
    print(f"代码审查完成: {review_result.content[:500]}...\n")
    
    # Step 4: 生成单元测试
    print("4. 生成单元测试...")
    testgen = TestGenTool()
    test_result = await testgen.handle_request({
        "files": [code_file],
        "model": "o3-mini",  # 使用O3-mini生成测试
        "test_type": "unit"
    })
    print(f"测试生成完成: {test_result.content[:500]}...\n")
    
    print("=== 工作流程完成 ===")
    
    # 返回综合结果
    return {
        "analysis": analysis_result.content,
        "gemini_feedback": gemini_feedback.content,
        "code_review": review_result.content,
        "tests": test_result.content
    }

# 使用示例
if __name__ == "__main__":
    # 替换为您要优化的代码文件路径
    code_file = "/path/to/your/code.py"
    
    # 运行工作流程
    results = asyncio.run(performance_optimization_workflow(code_file))
    
    # 保存结果
    with open("optimization_results.json", "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n结果已保存到 optimization_results.json")