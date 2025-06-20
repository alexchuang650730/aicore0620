#!/usr/bin/env python3
"""
Personal Product Orchestrator 測試腳本
測試使用personal目錄下的兩個AI引擎
"""

import asyncio
import json
import requests
import time
from datetime import datetime

def test_personal_orchestrator():
    """測試Personal Product Orchestrator"""
    
    print("=== Personal Product Orchestrator 測試開始 ===")
    
    # 測試數據
    test_request = {
        "user_id": "personal_test_user",
        "product_name": "AI驅動需求分析系統",
        "product_type": "web_application",
        "description": "這個核保的整份文件的sop 大概大概要花多少人處理表單,自動化比率在業界有多高,表單ocr 用人來審核在整個sop流程所佔的人月大概是多少",
        "requirements": {
            "functional": ["需求分析", "多模態處理", "智能推薦"],
            "non_functional": ["高性能", "可擴展", "安全性"],
            "constraints": ["預算限制", "時間限制"]
        },
        "priority": "high"
    }
    
    try:
        # 1. 測試健康檢查
        print("\n1. 測試健康檢查...")
        health_response = requests.get("http://localhost:5003/api/health", timeout=10)
        
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ 健康檢查成功: {health_data.get('service', 'Unknown')}")
            print(f"   版本: {health_data.get('version', 'Unknown')}")
            print(f"   引擎: {health_data.get('engines', [])}")
        else:
            print(f"❌ 健康檢查失敗: HTTP {health_response.status_code}")
            return False
        
        # 2. 創建產品項目
        print("\n2. 創建產品項目...")
        create_response = requests.post(
            "http://localhost:5003/api/create_product",
            json=test_request,
            timeout=30
        )
        
        if create_response.status_code == 200:
            create_data = create_response.json()
            if create_data.get("success"):
                project_id = create_data.get("project_id")
                print(f"✅ 項目創建成功: {project_id}")
            else:
                print(f"❌ 項目創建失敗: {create_data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ 項目創建請求失敗: HTTP {create_response.status_code}")
            return False
        
        # 3. 執行產品開發
        print("\n3. 執行產品開發...")
        execute_response = requests.post(
            f"http://localhost:5003/api/execute_development/{project_id}",
            timeout=60
        )
        
        if execute_response.status_code == 200:
            execute_data = execute_response.json()
            if execute_data.get("success"):
                project_data = execute_data.get("project", {})
                print(f"✅ 產品開發執行成功")
                print(f"   狀態: {project_data.get('status', 'Unknown')}")
                print(f"   進度: {project_data.get('progress', 0)}%")
                
                # 顯示結果摘要
                artifacts = project_data.get("artifacts", {})
                if artifacts:
                    print(f"\n📊 執行結果摘要:")
                    
                    # 多模態分析結果
                    multimodal = artifacts.get("multimodal_analysis", {})
                    if multimodal:
                        print(f"   多模態分析信心度: {multimodal.get('confidence_score', 0)}")
                        insights = multimodal.get('dynamic_insights', [])
                        print(f"   動態洞察數量: {len(insights)}")
                    
                    # 需求分析結果
                    requirement = artifacts.get("requirement_analysis", {})
                    if requirement:
                        print(f"   需求複雜度評分: {requirement.get('complexity_score', 0)}")
                        tech_reqs = requirement.get('technology_recommendations', [])
                        print(f"   技術建議數量: {len(tech_reqs)}")
                    
                    # 最終建議
                    final_rec = artifacts.get("final_recommendations", {})
                    if final_rec:
                        confidence = final_rec.get("confidence_metrics", {})
                        overall_conf = confidence.get("overall_confidence", 0)
                        print(f"   整體信心度: {overall_conf}")
                
            else:
                print(f"❌ 產品開發執行失敗: {execute_data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ 產品開發請求失敗: HTTP {execute_response.status_code}")
            return False
        
        # 4. 檢查項目狀態
        print("\n4. 檢查項目狀態...")
        status_response = requests.get(
            f"http://localhost:5003/api/project_status/{project_id}",
            timeout=10
        )
        
        if status_response.status_code == 200:
            status_data = status_response.json()
            if status_data.get("success"):
                status_info = status_data.get("status", {})
                print(f"✅ 項目狀態查詢成功")
                print(f"   項目ID: {status_info.get('project_id', 'Unknown')}")
                print(f"   狀態: {status_info.get('status', 'Unknown')}")
                print(f"   進度: {status_info.get('progress', 0)}%")
                
                workflows = status_info.get("workflows", [])
                print(f"   工作流狀態:")
                for workflow in workflows:
                    print(f"     - {workflow.get('type', 'Unknown')}: {workflow.get('status', 'Unknown')}")
            else:
                print(f"❌ 項目狀態查詢失敗: {status_data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ 項目狀態請求失敗: HTTP {status_response.status_code}")
            return False
        
        print("\n🎉 Personal Product Orchestrator 測試全部通過！")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 連接失敗: Personal Product Orchestrator 服務未啟動")
        return False
    except requests.exceptions.Timeout:
        print("❌ 請求超時: 服務響應時間過長")
        return False
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        return False

if __name__ == "__main__":
    success = test_personal_orchestrator()
    exit(0 if success else 1)

