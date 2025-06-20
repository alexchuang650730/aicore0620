#!/usr/bin/env python3
"""
簡單測試 - 檢查系統組件是否可用
"""

import sys
import os
from pathlib import Path

# 添加路徑
sys.path.append('/tmp/aicore0619')
sys.path.append('/home/ubuntu/enterprise_deployment')

def test_imports():
    """測試關鍵組件導入"""
    
    print("🔍 測試組件導入...")
    
    try:
        # 測試MCP協調器
        print("1. 測試MCP協調器...")
        from mcp.enhanced_mcp_coordinator import EnhancedMCPCoordinator
        print("   ✅ MCP協調器導入成功")
        
        # 測試KiloCode
        print("2. 測試KiloCode引擎...")
        from mcp.adapter.kilocode_mcp.kilocode_mcp import KiloCodeMCP
        print("   ✅ KiloCode引擎導入成功")
        
        # 測試工作流組件
        print("3. 測試工作流組件...")
        workflow_dir = Path('/tmp/aicore0619/mcp/workflow')
        if workflow_dir.exists():
            workflows = list(workflow_dir.iterdir())
            print(f"   ✅ 發現 {len(workflows)} 個工作流組件")
            for wf in workflows[:3]:  # 只顯示前3個
                print(f"      - {wf.name}")
        else:
            print("   ⚠️ 工作流目錄不存在")
        
        print("\n🎯 開始簡單功能測試...")
        
        # 測試MCP協調器初始化
        print("4. 測試MCP協調器初始化...")
        coordinator = EnhancedMCPCoordinator()
        print("   ✅ MCP協調器初始化成功")
        
        # 測試KiloCode初始化
        print("5. 測試KiloCode初始化...")
        kilocode = KiloCodeMCP()
        print("   ✅ KiloCode初始化成功")
        
        print("\n🎉 所有基礎組件測試通過！")
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\n✅ 系統基礎功能正常，可以進行進一步測試")
    else:
        print("\n❌ 系統存在問題，需要修復")

