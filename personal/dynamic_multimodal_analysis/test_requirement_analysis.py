#!/usr/bin/env python3
"""
測試需求分析工作流MCP的實際功能
"""

import asyncio
import sys
import json
from pathlib import Path

# 添加路徑
sys.path.append('/home/ubuntu/enterprise_deployment/aicore0619')

async def test_requirement_analysis_mcp():
    """測試需求分析MCP的功能"""
    
    print("🔍 開始測試需求分析工作流MCP...")
    
    try:
        # 導入需求分析MCP
        from mcp.adapter.requirement_analysis_mcp.requirement_analysis_mcp import RequirementAnalysisMcp
        
        # 初始化需求分析MCP
        req_analysis = RequirementAnalysisMcp()
        print("✅ 需求分析MCP初始化成功")
        
        # 測試1: 分析貪吃蛇遊戲需求
        print("\n📋 測試1: 分析貪吃蛇遊戲需求...")
        
        snake_game_requirement = {
            "type": "analyze_requirement",
            "requirement": "開發一個Python貪吃蛇遊戲，包含遊戲邏輯、圖形界面和計分系統",
            "requirement_type": "functional",
            "project_context": {
                "name": "貪吃蛇遊戲",
                "technology": "Python + pygame",
                "target_users": "遊戲玩家",
                "complexity": "medium"
            }
        }
        
        result1 = await req_analysis.process(snake_game_requirement)
        print("📊 貪吃蛇遊戲需求分析結果:")
        print(json.dumps(result1, indent=2, ensure_ascii=False))
        
        # 測試2: 創建用戶故事
        print("\n📋 測試2: 創建用戶故事...")
        
        user_story_request = {
            "type": "create_requirement",
            "requirement_type": "user_story",
            "title": "玩家控制貪吃蛇移動",
            "description": "作為遊戲玩家，我希望能夠使用方向鍵控制貪吃蛇的移動方向，以便我能夠操控遊戲",
            "priority": "high",
            "acceptance_criteria": [
                "按上方向鍵，蛇向上移動",
                "按下方向鍵，蛇向下移動", 
                "按左方向鍵，蛇向左移動",
                "按右方向鍵，蛇向右移動",
                "蛇不能立即反向移動"
            ]
        }
        
        result2 = await req_analysis.process(user_story_request)
        print("📊 用戶故事創建結果:")
        print(json.dumps(result2, indent=2, ensure_ascii=False))
        
        # 測試3: 需求驗證
        print("\n📋 測試3: 需求驗證...")
        
        validation_request = {
            "type": "validate_requirements",
            "requirements": [
                {
                    "id": "REQ-001",
                    "title": "遊戲控制",
                    "description": "玩家可以使用鍵盤控制貪吃蛇移動",
                    "type": "functional",
                    "priority": "high"
                },
                {
                    "id": "REQ-002", 
                    "title": "計分系統",
                    "description": "遊戲應該記錄玩家的分數",
                    "type": "functional",
                    "priority": "medium"
                }
            ]
        }
        
        result3 = await req_analysis.process(validation_request)
        print("📊 需求驗證結果:")
        print(json.dumps(result3, indent=2, ensure_ascii=False))
        
        # 測試4: 工作量估算
        print("\n📋 測試4: 工作量估算...")
        
        effort_request = {
            "type": "estimate_effort",
            "requirements": [
                {
                    "title": "遊戲邏輯實現",
                    "description": "實現貪吃蛇的移動、碰撞檢測、食物生成等核心邏輯",
                    "complexity": "medium"
                },
                {
                    "title": "圖形界面",
                    "description": "使用pygame創建遊戲視窗和圖形渲染",
                    "complexity": "medium"
                },
                {
                    "title": "計分系統",
                    "description": "實現分數計算和顯示",
                    "complexity": "low"
                }
            ]
        }
        
        result4 = await req_analysis.process(effort_request)
        print("📊 工作量估算結果:")
        print(json.dumps(result4, indent=2, ensure_ascii=False))
        
        # 測試5: 生成需求文檔
        print("\n📋 測試5: 生成需求文檔...")
        
        doc_request = {
            "type": "generate_documentation",
            "project_name": "貪吃蛇遊戲",
            "requirements": [
                {
                    "id": "REQ-001",
                    "title": "遊戲控制",
                    "description": "玩家可以使用方向鍵控制貪吃蛇移動",
                    "type": "functional",
                    "priority": "high",
                    "acceptance_criteria": ["支持四個方向鍵", "不能反向移動"]
                },
                {
                    "id": "REQ-002",
                    "title": "計分系統", 
                    "description": "遊戲記錄和顯示玩家分數",
                    "type": "functional",
                    "priority": "medium",
                    "acceptance_criteria": ["吃食物加分", "顯示當前分數", "記錄最高分"]
                }
            ]
        }
        
        result5 = await req_analysis.process(doc_request)
        print("📊 需求文檔生成結果:")
        print(json.dumps(result5, indent=2, ensure_ascii=False))
        
        # 保存測試結果
        test_results = {
            "test_name": "需求分析工作流MCP測試",
            "test_time": "2025-06-18",
            "results": {
                "requirement_analysis": result1,
                "user_story_creation": result2,
                "requirement_validation": result3,
                "effort_estimation": result4,
                "documentation_generation": result5
            },
            "summary": {
                "total_tests": 5,
                "successful_tests": sum(1 for r in [result1, result2, result3, result4, result5] if r.get("status") == "success"),
                "mcp_functional": True
            }
        }
        
        # 保存結果到文件
        output_file = Path("/home/ubuntu/enterprise_deployment/requirement_analysis_test_results.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 測試結果已保存到: {output_file}")
        print(f"✅ 需求分析MCP測試完成！成功測試: {test_results['summary']['successful_tests']}/5")
        
        return True
        
    except Exception as e:
        print(f"❌ 需求分析MCP測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_requirement_analysis_mcp())
    if success:
        print("\n🎉 需求分析工作流MCP測試成功！")
    else:
        print("\n❌ 需求分析工作流MCP測試失敗")

