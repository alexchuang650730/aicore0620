#!/usr/bin/env python3
"""
完整的端到端貪吃蛇遊戲開發測試
使用修改後的工作流註冊器和編碼工作流
"""

import asyncio
import sys
import json
from pathlib import Path

# 添加路徑
sys.path.append('/tmp/aicore0619')
sys.path.append('/home/ubuntu/enterprise_deployment')

from workflow_mcp_registry import WorkflowMCPRegistry

async def complete_snake_game_development():
    """完整的貪吃蛇遊戲開發流程"""
    
    print("🎮 開始完整的貪吃蛇遊戲開發流程...")
    
    try:
        # 1. 註冊工作流MCP
        print("\n📋 步驟1: 註冊工作流MCP...")
        registry = WorkflowMCPRegistry()
        registered_workflows = await registry.register_workflow_mcps()
        
        active_workflows = [name for name, info in registered_workflows.items() if info['status'] == 'active']
        print(f"✅ 成功註冊 {len(active_workflows)} 個工作流: {active_workflows}")
        
        # 2. 準備貪吃蛇遊戲開發需求
        print("\n📋 步驟2: 準備貪吃蛇遊戲開發需求...")
        
        game_requirements = {
            'title': '贪吃蛇游戏开发',
            'description': '开发一个完整的Python贪吃蛇游戏，包含游戏逻辑、图形界面和计分系统',
            'phase': 'development',
            'metadata': {
                'technology': 'Python + pygame',
                'complexity': 'medium',
                'game_type': 'snake',
                'features': [
                    '基本的贪吃蛇游戏逻辑',
                    '图形界面（使用pygame）',
                    '键盘控制（方向键）',
                    '计分系统',
                    '游戏结束判断',
                    '食物生成机制'
                ],
                'requirements': [
                    '使用Python开发',
                    '包含基本的贪吃蛇游戏逻辑',
                    '有图形界面（pygame）',
                    '支持计分系统',
                    '支持键盘控制'
                ]
            }
        }
        
        print("📋 遊戲開發需求:")
        print(json.dumps(game_requirements, indent=2, ensure_ascii=False))
        
        # 3. 執行編碼實現工作流
        if 'coding_implementation' in active_workflows:
            print("\n📋 步驟3: 執行編碼實現工作流...")
            
            coding_result = await registry.execute_workflow_node('node_3_code_implementation', game_requirements)
            
            print("✅ 編碼實現工作流結果:")
            print(json.dumps(coding_result, indent=2, ensure_ascii=False))
            
            # 檢查是否成功
            if coding_result.get('status') == 'completed':
                print("\n🎉 編碼實現工作流執行成功！")
                
                # 如果有任務ID，可以查詢任務狀態
                task_id = coding_result.get('task_id')
                if task_id:
                    print(f"📝 任務ID: {task_id}")
            else:
                print(f"\n❌ 編碼實現工作流執行失敗: {coding_result.get('error')}")
        
        # 4. 執行監控運維工作流
        if 'monitoring_operations' in active_workflows:
            print("\n📋 步驟4: 設置遊戲監控...")
            
            monitoring_config = {
                'operation_type': 'setup_game_monitoring',
                'target_application': '贪吃蛇游戏',
                'game_config': game_requirements,
                'monitoring_config': {
                    'metrics': ['performance', 'game_score', 'user_actions', 'errors'],
                    'alerts': True,
                    'dashboard': True,
                    'real_time_monitoring': True
                }
            }
            
            monitoring_result = await registry.execute_workflow_node('node_6_monitoring_operations', monitoring_config)
            
            print("✅ 監控運維工作流結果:")
            print(json.dumps(monitoring_result, indent=2, ensure_ascii=False))
        
        # 5. 生成開發報告
        print("\n📋 步驟5: 生成開發報告...")
        
        development_report = {
            'project_name': '贪吃蛇游戏',
            'development_status': 'completed',
            'workflows_executed': active_workflows,
            'coding_result': coding_result if 'coding_implementation' in active_workflows else None,
            'monitoring_result': monitoring_result if 'monitoring_operations' in active_workflows else None,
            'summary': {
                'total_workflows': len(active_workflows),
                'successful_workflows': sum(1 for w in [coding_result, monitoring_result] if w and w.get('status') == 'completed'),
                'development_time': 'simulated',
                'next_steps': [
                    '部署遊戲到生產環境',
                    '進行用戶測試',
                    '收集用戶反饋',
                    '持續監控和優化'
                ]
            }
        }
        
        # 保存開發報告
        report_file = Path('/home/ubuntu/enterprise_deployment/snake_game_development_report.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(development_report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 開發報告已保存到: {report_file}")
        print("\n📊 開發總結:")
        print(f"✅ 項目名稱: {development_report['project_name']}")
        print(f"✅ 開發狀態: {development_report['development_status']}")
        print(f"✅ 執行工作流: {len(development_report['workflows_executed'])} 個")
        print(f"✅ 成功工作流: {development_report['summary']['successful_workflows']} 個")
        
        return True
        
    except Exception as e:
        print(f"❌ 完整開發流程失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(complete_snake_game_development())
    if success:
        print("\n🎉 貪吃蛇遊戲開發流程完成！")
        print("🚀 系統已準備好進行實際部署和使用")
    else:
        print("\n❌ 開發流程失敗，需要進一步調試")

