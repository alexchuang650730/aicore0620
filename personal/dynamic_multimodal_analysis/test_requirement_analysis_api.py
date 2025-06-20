#!/usr/bin/env python3
"""
通過HTTP API測試需求分析MCP
"""

import requests
import json
import time

def test_requirement_analysis_api():
    """測試需求分析MCP的HTTP API"""
    
    base_url = "http://localhost:8100"
    
    print("🔍 開始測試需求分析MCP HTTP API...")
    
    # 等待服務器啟動
    print("⏳ 等待服務器啟動...")
    time.sleep(3)
    
    try:
        # 測試1: 健康檢查
        print("\n📋 測試1: 健康檢查...")
        response = requests.get(f"{base_url}/health")
        print(f"狀態碼: {response.status_code}")
        print(f"響應: {response.json()}")
        
        # 測試2: 獲取MCP信息
        print("\n📋 測試2: 獲取MCP信息...")
        response = requests.get(f"{base_url}/api/info")
        print(f"狀態碼: {response.status_code}")
        print(f"響應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # 測試3: 測試貪吃蛇遊戲需求分析
        print("\n📋 測試3: 貪吃蛇遊戲需求分析...")
        response = requests.post(f"{base_url}/api/test/snake-game")
        print(f"狀態碼: {response.status_code}")
        print(f"響應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # 測試4: 自定義需求分析
        print("\n📋 測試4: 自定義需求分析...")
        custom_data = {
            "requirement": "開發一個在線購物網站，支持用戶註冊、商品瀏覽、購物車和支付功能",
            "requirement_type": "functional",
            "project_context": {
                "name": "電商網站",
                "technology": "React + Node.js",
                "target_users": "在線購物用戶",
                "complexity": "high"
            }
        }
        
        response = requests.post(f"{base_url}/api/analyze", json=custom_data)
        print(f"狀態碼: {response.status_code}")
        print(f"響應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # 測試5: 創建用戶故事
        print("\n📋 測試5: 創建用戶故事...")
        user_story_data = {
            "requirement_type": "user_story",
            "title": "用戶登錄功能",
            "description": "作為網站用戶，我希望能夠使用郵箱和密碼登錄系統，以便訪問個人化功能",
            "priority": "high",
            "acceptance_criteria": [
                "用戶可以輸入郵箱和密碼",
                "系統驗證用戶憑證",
                "登錄成功後跳轉到用戶儀表板",
                "登錄失敗顯示錯誤信息"
            ]
        }
        
        response = requests.post(f"{base_url}/api/create", json=user_story_data)
        print(f"狀態碼: {response.status_code}")
        print(f"響應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # 測試6: 需求驗證
        print("\n📋 測試6: 需求驗證...")
        validation_data = {
            "requirements": [
                {
                    "id": "REQ-001",
                    "title": "用戶登錄",
                    "description": "用戶可以使用郵箱和密碼登錄系統",
                    "type": "functional",
                    "priority": "high"
                },
                {
                    "id": "REQ-002",
                    "title": "商品搜索",
                    "description": "用戶可以搜索商品",
                    "type": "functional",
                    "priority": "medium"
                }
            ]
        }
        
        response = requests.post(f"{base_url}/api/validate", json=validation_data)
        print(f"狀態碼: {response.status_code}")
        print(f"響應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # 測試7: 工作量估算
        print("\n📋 測試7: 工作量估算...")
        effort_data = {
            "requirements": [
                {
                    "title": "用戶認證系統",
                    "description": "實現用戶註冊、登錄、密碼重置功能",
                    "complexity": "medium"
                },
                {
                    "title": "商品管理系統",
                    "description": "實現商品CRUD操作、分類管理、庫存管理",
                    "complexity": "high"
                },
                {
                    "title": "支付集成",
                    "description": "集成第三方支付系統",
                    "complexity": "high"
                }
            ]
        }
        
        response = requests.post(f"{base_url}/api/estimate", json=effort_data)
        print(f"狀態碼: {response.status_code}")
        print(f"響應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        print("\n🎉 需求分析MCP HTTP API測試完成！")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到服務器，請確保服務器已啟動")
        return False
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        return False

if __name__ == "__main__":
    success = test_requirement_analysis_api()
    if success:
        print("\n✅ 需求分析MCP HTTP API測試成功！")
    else:
        print("\n❌ 需求分析MCP HTTP API測試失敗")

