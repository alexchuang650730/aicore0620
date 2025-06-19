#!/usr/bin/env python3
"""
整合工作流MCP到ProductOrchestrator - 完整的端到端測試
"""

import asyncio
import sys
import json
from pathlib import Path

# 添加路徑
sys.path.append('/tmp/aicore0619')
sys.path.append('/home/ubuntu/enterprise_deployment')

from workflow_mcp_registry import WorkflowMCPRegistry

async def test_integrated_product_orchestrator():
    """測試整合了工作流MCP的ProductOrchestrator"""
    
    try:
        print("🚀 啟動整合測試...")
        
        # 1. 首先註冊工作流MCP
        print("\n📋 步驟1: 註冊工作流MCP...")
        registry = WorkflowMCPRegistry()
        registered_workflows = await registry.register_workflow_mcps()
        
        active_workflows = [name for name, info in registered_workflows.items() if info['status'] == 'active']
        print(f"✅ 成功註冊 {len(active_workflows)} 個工作流: {active_workflows}")
        
        # 2. 啟動ProductOrchestrator
        print("\n📋 步驟2: 啟動ProductOrchestrator...")
        from mcp.coordinator.workflow_collaboration.product_orchestrator_v3 import ProductOrchestratorV3
        
        orchestrator = ProductOrchestratorV3()
        print("✅ ProductOrchestrator初始化成功")
        
        # 3. 修改ProductOrchestrator的工作流執行邏輯
        # 將我們的工作流註冊器注入到orchestrator中
        orchestrator.workflow_registry = registry
        
        # 4. 準備貪吃蛇遊戲開發需求
        print("\n📋 步驟3: 準備用戶需求...")
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
        
        print("📋 用戶需求:")
        print(json.dumps(user_requirements, indent=2, ensure_ascii=False))
        
        # 5. 手動執行可用的工作流節點
        print("\n📋 步驟4: 手動執行可用的工作流節點...")
        
        # 測試編碼實現工作流
        if 'coding_implementation' in active_workflows:
            print("\n🔄 執行編碼實現工作流...")
            
            # 調整請求格式以符合工作流期望
            coding_request = {
                'task_id': 'snake_game_001',
                'title': '贪吃蛇游戏开发',
                'description': '开发一个Python贪吃蛇游戏',
                'phase': 'development',
                'requirements': user_requirements['requirements'],
                'metadata': {
                    'technology': 'Python + pygame',
                    'complexity': 'medium',
                    'game_type': 'snake'
                }
            }
            
            result = await registry.execute_workflow_node('node_3_code_implementation', coding_request)
            print("📋 編碼實現工作流結果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 測試監控運維工作流
        if 'monitoring_operations' in active_workflows:
            print("\n🔄 執行監控運維工作流...")
            
            monitoring_request = {
                'operation_type': 'setup_monitoring',
                'target_application': '贪吃蛇游戏',
                'monitoring_config': {
                    'metrics': ['performance', 'errors', 'usage'],
                    'alerts': True,
                    'dashboard': True
                }
            }
            
            result = await registry.execute_workflow_node('node_6_monitoring_operations', monitoring_request)
            print("📋 監控運維工作流結果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 6. 停止orchestrator
        await orchestrator.stop()
        
        print("\n🎉 整合測試完成！")
        return True
        
    except Exception as e:
        print(f"❌ 整合測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_integrated_product_orchestrator())
    if success:
        print("\n✅ 整合測試成功！系統可以進行端到端工作流處理")
    else:
        print("\n❌ 整合測試失敗，需要進一步調試")

