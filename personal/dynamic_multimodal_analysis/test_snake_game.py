#!/usr/bin/env python3
"""
測試貪吃蛇遊戲開發 - 使用ProductOrchestrator
"""

import asyncio
import sys
import json
from pathlib import Path

# 添加路徑
sys.path.append('/tmp/aicore0619')
sys.path.append('/home/ubuntu/enterprise_deployment')

async def test_snake_game_development():
    """測試貪吃蛇遊戲開發流程"""
    
    try:
        # 導入ProductOrchestrator
        from mcp.coordinator.workflow_collaboration.product_orchestrator_v3 import ProductOrchestratorV3
        
        print("🚀 啟動ProductOrchestrator...")
        orchestrator = ProductOrchestratorV3()
        
        # 準備用戶需求
        user_requirements = {
            'name': '貪吃蛇遊戲',
            'description': '開發一個Python貪吃蛇遊戲，包含遊戲邏輯、圖形界面和計分系統',
            'type': 'game_development',
            'complexity': 'medium',
            'priority': 'high',
            'requirements': [
                '使用Python開發',
                '包含基本的貪吃蛇遊戲邏輯',
                '有圖形界面',
                '支持計分系統',
                '支持鍵盤控制'
            ]
        }
        
        print("📋 用戶需求:")
        print(json.dumps(user_requirements, indent=2, ensure_ascii=False))
        
        # 執行工作流
        print("\n🔄 開始執行工作流...")
        result = await orchestrator.create_and_execute_workflow(user_requirements)
        
        print("\n✅ 工作流執行結果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 停止orchestrator
        await orchestrator.stop()
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_snake_game_development())

