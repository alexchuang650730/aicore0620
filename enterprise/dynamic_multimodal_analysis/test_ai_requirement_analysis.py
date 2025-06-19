#!/usr/bin/env python3
"""
測試AI增強的需求分析MCP
"""

import asyncio
import json
import sys
from pathlib import Path

# 添加路徑
sys.path.append('/home/ubuntu/enterprise_deployment')

async def test_ai_requirement_analysis():
    """測試AI增強的需求分析MCP"""
    
    print("🤖 開始測試AI增強的需求分析MCP...")
    
    try:
        # 導入AI需求分析MCP
        from ai_requirement_analysis_mcp import AIRequirementAnalysisMcp
        
        # 初始化AI需求分析MCP
        ai_req_analysis = AIRequirementAnalysisMcp({
            "primary_model": "gpt-4",
            "fallback_model": "claude-3-sonnet"
        })
        print("✅ AI需求分析MCP初始化成功")
        
        # 測試1: AI分析貪吃蛇遊戲需求
        print("\n🧠 測試1: AI分析貪吃蛇遊戲需求...")
        
        snake_game_requirement = {
            "type": "analyze_requirement",
            "requirement": "開發一個Python貪吃蛇遊戲，包含遊戲邏輯、圖形界面和計分系統，支持方向鍵控制，碰撞檢測，食物隨機生成，分數統計和遊戲結束判斷",
            "requirement_type": "functional",
            "project_context": {
                "name": "貪吃蛇遊戲",
                "technology": "Python + pygame",
                "target_users": "休閒遊戲玩家",
                "complexity": "medium",
                "timeline": "2週",
                "team_size": 2
            }
        }
        
        result1 = await ai_req_analysis.process(snake_game_requirement)
        print("📊 AI貪吃蛇遊戲需求分析結果:")
        print(json.dumps(result1, indent=2, ensure_ascii=False))
        
        # 測試2: AI創建用戶故事
        print("\n🧠 測試2: AI創建用戶故事...")
        
        user_story_request = {
            "type": "create_requirement",
            "requirement_type": "user_story",
            "title": "玩家控制貪吃蛇移動",
            "description": "作為遊戲玩家，我希望能夠使用方向鍵控制貪吃蛇的移動方向，以便我能夠靈活操控遊戲角色避開障礙並吃到食物"
        }
        
        result2 = await ai_req_analysis.process(user_story_request)
        print("📊 AI用戶故事創建結果:")
        print(json.dumps(result2, indent=2, ensure_ascii=False))
        
        # 測試3: AI需求驗證
        print("\n🧠 測試3: AI需求驗證...")
        
        validation_request = {
            "type": "validate_requirements",
            "requirements": [
                {
                    "id": "REQ-001",
                    "title": "遊戲控制系統",
                    "description": "玩家可以使用方向鍵控制貪吃蛇移動",
                    "type": "functional",
                    "priority": "high"
                },
                {
                    "id": "REQ-002", 
                    "title": "計分系統",
                    "description": "遊戲應該記錄玩家的分數並顯示",
                    "type": "functional",
                    "priority": "medium"
                },
                {
                    "id": "REQ-003",
                    "title": "性能要求",
                    "description": "遊戲應該流暢運行",
                    "type": "non_functional",
                    "priority": "high"
                }
            ]
        }
        
        result3 = await ai_req_analysis.process(validation_request)
        print("📊 AI需求驗證結果:")
        print(json.dumps(result3, indent=2, ensure_ascii=False))
        
        # 測試4: AI工作量估算
        print("\n🧠 測試4: AI工作量估算...")
        
        effort_request = {
            "type": "estimate_effort",
            "requirements": [
                {
                    "title": "遊戲邏輯引擎",
                    "description": "實現貪吃蛇的移動、碰撞檢測、食物生成等核心邏輯",
                    "complexity": "medium"
                },
                {
                    "title": "圖形渲染系統",
                    "description": "使用pygame創建遊戲視窗、繪製蛇身、食物和界面元素",
                    "complexity": "medium"
                },
                {
                    "title": "用戶輸入處理",
                    "description": "處理鍵盤輸入，實現方向控制和遊戲操作",
                    "complexity": "low"
                },
                {
                    "title": "計分和狀態管理",
                    "description": "實現分數計算、遊戲狀態管理和數據持久化",
                    "complexity": "low"
                }
            ]
        }
        
        result4 = await ai_req_analysis.process(effort_request)
        print("📊 AI工作量估算結果:")
        print(json.dumps(result4, indent=2, ensure_ascii=False))
        
        # 測試5: AI需求優先級排序
        print("\n🧠 測試5: AI需求優先級排序...")
        
        prioritization_request = {
            "type": "prioritize_requirements",
            "requirements": [
                {
                    "id": "REQ-001",
                    "title": "基礎遊戲邏輯",
                    "description": "蛇的移動和基本遊戲規則",
                    "business_value": 9,
                    "complexity": 6
                },
                {
                    "id": "REQ-002",
                    "title": "圖形界面",
                    "description": "遊戲的視覺呈現",
                    "business_value": 8,
                    "complexity": 5
                },
                {
                    "id": "REQ-003",
                    "title": "計分系統",
                    "description": "分數計算和顯示",
                    "business_value": 6,
                    "complexity": 3
                },
                {
                    "id": "REQ-004",
                    "title": "音效系統",
                    "description": "遊戲音效和背景音樂",
                    "business_value": 4,
                    "complexity": 4
                }
            ],
            "business_context": {
                "project_deadline": "2週",
                "team_experience": "中等",
                "budget_constraint": "有限"
            }
        }
        
        result5 = await ai_req_analysis.process(prioritization_request)
        print("📊 AI需求優先級排序結果:")
        print(json.dumps(result5, indent=2, ensure_ascii=False))
        
        # 測試6: AI生成需求文檔
        print("\n🧠 測試6: AI生成需求文檔...")
        
        doc_request = {
            "type": "generate_documentation",
            "project_name": "Python貪吃蛇遊戲",
            "document_type": "comprehensive",
            "requirements": [
                {
                    "id": "REQ-001",
                    "title": "遊戲控制系統",
                    "description": "玩家使用方向鍵控制貪吃蛇移動",
                    "type": "functional",
                    "priority": "high",
                    "acceptance_criteria": ["支持上下左右四個方向", "響應時間小於100ms", "不能反向移動"]
                },
                {
                    "id": "REQ-002",
                    "title": "計分系統",
                    "description": "記錄和顯示玩家分數",
                    "type": "functional", 
                    "priority": "medium",
                    "acceptance_criteria": ["吃食物加10分", "實時顯示分數", "記錄最高分"]
                }
            ]
        }
        
        result6 = await ai_req_analysis.process(doc_request)
        print("📊 AI需求文檔生成結果:")
        print(json.dumps(result6, indent=2, ensure_ascii=False))
        
        # 獲取AI MCP狀態
        print("\n🧠 AI MCP狀態信息...")
        status = await ai_req_analysis.get_status()
        print("📊 AI MCP狀態:")
        print(json.dumps(status, indent=2, ensure_ascii=False))
        
        # 保存測試結果
        test_results = {
            "test_name": "AI增強需求分析MCP測試",
            "test_time": "2025-06-18",
            "ai_capabilities": True,
            "results": {
                "ai_requirement_analysis": result1,
                "ai_user_story_creation": result2,
                "ai_requirement_validation": result3,
                "ai_effort_estimation": result4,
                "ai_prioritization": result5,
                "ai_documentation": result6
            },
            "performance_stats": status.get("performance_stats", {}),
            "summary": {
                "total_tests": 6,
                "successful_tests": sum(1 for r in [result1, result2, result3, result4, result5, result6] if r.get("status") == "success"),
                "ai_enhanced": True,
                "quantitative_analysis": True
            }
        }
        
        # 保存結果到文件
        output_file = Path("/home/ubuntu/enterprise_deployment/ai_requirement_analysis_test_results.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 AI測試結果已保存到: {output_file}")
        print(f"✅ AI需求分析MCP測試完成！成功測試: {test_results['summary']['successful_tests']}/6")
        
        return True
        
    except Exception as e:
        print(f"❌ AI需求分析MCP測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_ai_requirement_analysis())
    if success:
        print("\n🎉 AI增強需求分析MCP測試成功！")
        print("🤖 現在具備真正的AI分析能力！")
    else:
        print("\n❌ AI增強需求分析MCP測試失敗")

