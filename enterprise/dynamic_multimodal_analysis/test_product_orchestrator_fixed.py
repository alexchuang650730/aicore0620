#!/usr/bin/env python3
"""
測試修改後的ProductOrchestrator - 移除smart_routing_system依賴
"""

import asyncio
import sys
import json
from pathlib import Path

# 添加路徑
sys.path.append('/tmp/aicore0619')
sys.path.append('/home/ubuntu/enterprise_deployment')

async def test_product_orchestrator_without_smart_routing():
    """測試移除smart_routing_system後的ProductOrchestrator"""
    
    try:
        print("🚀 啟動修改後的ProductOrchestrator...")
        
        # 導入修改後的ProductOrchestrator
        from mcp.coordinator.workflow_collaboration.product_orchestrator_v3 import ProductOrchestratorV3
        
        orchestrator = ProductOrchestratorV3()
        print("✅ ProductOrchestrator初始化成功（無smart_routing_system依賴）")
        
        # 準備貪吃蛇遊戲開發需求
        user_requirements = {
            'name': '贪吃蛇游戏',
            'description': '开发一个Python贪吃蛇游戏，包含游戏逻辑、图形界面和计分系统',
            'type': 'game_development',
            'complexity': 'medium',
            'priority': 'high',
            'requirements': [
                '使用Python开发',
                '包含基本的贪吃蛇游戏逻辑',
                '有图形界面（pygame）',
                '支持计分系统',
                '支持键盘控制'
            ]
        }
        
        print("\n📋 用戶需求:")
        print(json.dumps(user_requirements, indent=2, ensure_ascii=False))
        
        # 測試工作流創建和執行
        print("\n🔄 開始執行工作流...")
        result = await orchestrator.create_and_execute_workflow(user_requirements)
        
        print("\n✅ 工作流執行結果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 停止orchestrator
        await orchestrator.stop()
        
        return True
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_product_orchestrator_without_smart_routing())
    if success:
        print("\n🎉 ProductOrchestrator修改成功，可以正常運行！")
    else:
        print("\n❌ ProductOrchestrator修改失敗")

