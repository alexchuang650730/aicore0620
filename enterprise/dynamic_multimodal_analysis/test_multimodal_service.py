#!/usr/bin/env python3
"""
測試多模態需求分析HTTP服務
"""

import requests
import json
import time
import os
from pathlib import Path

# 服務地址
BASE_URL = "http://localhost:8300"

def test_health_check():
    """測試健康檢查"""
    print("🔍 測試健康檢查...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康檢查成功: {data['status']}")
            print(f"📊 組件狀態: {data['components']}")
            return True
        else:
            print(f"❌ 健康檢查失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康檢查異常: {e}")
        return False

def test_service_info():
    """測試服務信息"""
    print("\\n📋 測試服務信息...")
    try:
        response = requests.get(f"{BASE_URL}/api/info")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 服務名稱: {data['service_name']}")
            print(f"📝 功能列表: {data['features']}")
            print(f"📄 支持格式: {data['supported_formats']}")
            return True
        else:
            print(f"❌ 服務信息獲取失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 服務信息異常: {e}")
        return False

def test_start_session():
    """測試開始會話"""
    print("\\n🚀 測試開始需求分析會話...")
    try:
        data = {
            "requirement": "我需要開發一個在線購物網站，包含用戶註冊、商品展示、購物車和支付功能"
        }
        
        response = requests.post(f"{BASE_URL}/api/start-session", json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 會話創建成功: {result['session_id']}")
            print(f"🎯 置信度: {result['initial_analysis']['confidence_level']}")
            print(f"❓ 待回答問題數: {len(result['initial_analysis']['pending_questions'])}")
            
            # 顯示前3個問題
            questions = result['initial_analysis']['pending_questions'][:3]
            for i, q in enumerate(questions, 1):
                print(f"  {i}. [{q['urgency']}] {q['question']}")
            
            return result['session_id']
        else:
            print(f"❌ 會話創建失敗: {response.status_code}")
            print(f"錯誤: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 會話創建異常: {e}")
        return None

def test_analyze_text(session_id=None):
    """測試文本分析"""
    print("\\n📝 測試文本需求分析...")
    try:
        data = {
            "text": "用戶可以瀏覽商品分類，查看商品詳情，添加到購物車，並進行結算支付。系統需要支持多種支付方式，包括信用卡和電子錢包。",
            "session_id": session_id
        }
        
        response = requests.post(f"{BASE_URL}/api/analyze-text", json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 文本分析成功")
            print(f"📊 會話ID: {result['session_id']}")
            if 'analysis' in result:
                print(f"🎯 分析結果: {str(result['analysis'])[:200]}...")
            return result['session_id']
        else:
            print(f"❌ 文本分析失敗: {response.status_code}")
            print(f"錯誤: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 文本分析異常: {e}")
        return None

def test_upload_document():
    """測試文檔上傳"""
    print("\\n📄 測試文檔上傳分析...")
    
    # 創建測試文檔
    test_content = """
需求規格書

1. 項目概述
   開發一個現代化的電子商務平台

2. 功能需求
   - 用戶管理：註冊、登錄、個人資料管理
   - 商品管理：商品展示、分類、搜索
   - 購物車：添加商品、修改數量、刪除商品
   - 訂單管理：下單、支付、訂單跟蹤
   - 支付系統：支持多種支付方式

3. 非功能需求
   - 性能：支持1000並發用戶
   - 安全：數據加密、安全支付
   - 可用性：99.9%正常運行時間
"""
    
    # 保存測試文檔
    test_file_path = "/tmp/test_requirement.txt"
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    try:
        with open(test_file_path, 'rb') as f:
            files = {'file': ('test_requirement.txt', f, 'text/plain')}
            data = {'session_id': ''}  # 新會話
            
            response = requests.post(f"{BASE_URL}/api/upload-document", files=files, data=data)
            
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 文檔上傳成功")
            print(f"📊 會話ID: {result['session_id']}")
            print(f"📄 文件名: {result['filename']}")
            
            # 顯示文檔處理結果
            if 'document_processing' in result:
                processing = result['document_processing']
                print(f"📝 文檔類型: {processing.get('type', 'unknown')}")
                if 'metadata' in processing:
                    metadata = processing['metadata']
                    print(f"📊 文檔統計: {metadata.get('word_count', 0)} 詞, {metadata.get('line_count', 0)} 行")
            
            return result['session_id']
        else:
            print(f"❌ 文檔上傳失敗: {response.status_code}")
            print(f"錯誤: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 文檔上傳異常: {e}")
        return None
    finally:
        # 清理測試文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

def test_get_session(session_id):
    """測試獲取會話狀態"""
    if not session_id:
        print("\\n⚠️ 跳過會話狀態測試（無有效會話ID）")
        return
    
    print("\\n📊 測試獲取會話狀態...")
    try:
        response = requests.get(f"{BASE_URL}/api/get-session", params={'session_id': session_id})
        if response.status_code == 200:
            result = response.json()
            session = result['session']
            print(f"✅ 會話狀態獲取成功")
            print(f"🎯 置信度: {session['confidence_level']}")
            print(f"✅ 已完成方面: {len(session['completed_aspects'])}")
            print(f"❓ 待回答問題: {len(session['pending_questions'])}")
            print(f"💬 對話輪次: {len(session['conversation_history'])}")
            return True
        else:
            print(f"❌ 會話狀態獲取失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 會話狀態異常: {e}")
        return False

def test_list_sessions():
    """測試列出活躍會話"""
    print("\\n📋 測試列出活躍會話...")
    try:
        response = requests.get(f"{BASE_URL}/api/sessions")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 活躍會話列表獲取成功")
            print(f"📊 活躍會話數: {result['active_sessions_count']}")
            
            for session in result['sessions'][:3]:  # 顯示前3個會話
                print(f"  - {session['session_id'][:8]}... (置信度: {session['confidence_level']})")
            
            return True
        else:
            print(f"❌ 會話列表獲取失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 會話列表異常: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 開始測試多模態需求分析HTTP服務")
    print("=" * 60)
    
    # 等待服務啟動
    print("⏳ 等待服務啟動...")
    time.sleep(2)
    
    # 測試序列
    session_id = None
    
    # 1. 健康檢查
    if not test_health_check():
        print("❌ 服務未正常運行，停止測試")
        return
    
    # 2. 服務信息
    test_service_info()
    
    # 3. 開始會話
    session_id = test_start_session()
    
    # 4. 文本分析
    if session_id:
        session_id = test_analyze_text(session_id) or session_id
    
    # 5. 文檔上傳
    doc_session_id = test_upload_document()
    
    # 6. 獲取會話狀態
    test_get_session(session_id or doc_session_id)
    
    # 7. 列出會話
    test_list_sessions()
    
    print("\\n" + "=" * 60)
    print("🎉 測試完成！")

if __name__ == "__main__":
    main()

