#!/usr/bin/env python3
"""
測試真實用戶請求的動態MCP創建
"""

import sys
import asyncio
sys.path.append('/home/ubuntu/enterprise_deployment')

from mcp.coordinator.unified_system_coordinator_mcp import UnifiedSystemCoordinatorMCP

async def test_real_user_requests():
    """測試真實用戶請求"""
    coordinator = UnifiedSystemCoordinatorMCP()
    
    # 初始化系統
    print("=== 初始化系統 ===")
    init_result = await coordinator.handle_request("initialize_system", {})
    print(f"初始化結果: {init_result['status']}")
    
    # 測試真實用戶請求
    test_requests = [
        "我想開發一個個人部落格網站",
        "幫我分析這個項目的需求",
        "設計一個電商系統的架構",
        "我需要測試我的應用程式",
        "幫我部署這個系統到生產環境"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n=== 測試請求 {i}: {request} ===")
        
        result = await coordinator.handle_request("process_user_request", {
            "user_input": request,
            "user_context": {"test_mode": True}
        })
        
        print(f"處理狀態: {result['status']}")
        if result['status'] == 'success':
            print(f"✅ 成功處理")
            if 'steps' in result:
                for step in result['steps']:
                    print(f"  - {step['step']}: {step['result']['status']}")
        else:
            print(f"❌ 處理失敗: {result.get('failure_reason', '未知原因')}")
            # 如果失敗，嘗試觸發動態創建
            if 'failure_reason' in result and '沒有選擇到合適的工作流' in result['failure_reason']:
                print("  → 觸發動態MCP創建...")
                # 這裡可以添加動態創建邏輯

if __name__ == "__main__":
    asyncio.run(test_real_user_requests())

