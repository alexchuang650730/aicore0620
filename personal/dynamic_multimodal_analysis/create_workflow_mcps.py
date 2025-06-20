#!/usr/bin/env python3
"""
創建多個工作流MCP的批量腳本
"""

import sys
import os
import asyncio
sys.path.append('/home/ubuntu/enterprise_deployment')

from mcp.coordinator.dynamic_mcp_creator_mcp import DynamicMCPCreatorMCP

async def create_multiple_workflow_mcps():
    """創建多個工作流MCP"""
    creator = DynamicMCPCreatorMCP()
    
    # 要創建的工作流MCP列表
    workflow_specs = [
        {
            "intent_description": "開發Web應用程式",
            "expected_mcp_name": "web_application_mcp",
            "intent_scope": {
                "primary_scope": "Web應用開發",
                "secondary_scopes": ["前端開發", "後端開發", "數據庫設計"]
            }
        },
        {
            "intent_description": "分析數據和生成報告",
            "expected_mcp_name": "data_analysis_mcp", 
            "intent_scope": {
                "primary_scope": "數據分析",
                "secondary_scopes": ["統計分析", "數據可視化", "報告生成"]
            }
        },
        {
            "intent_description": "系統架構設計",
            "expected_mcp_name": "system_architecture_mcp",
            "intent_scope": {
                "primary_scope": "系統架構",
                "secondary_scopes": ["技術選型", "架構設計", "性能優化"]
            }
        }
    ]
    
    created_mcps = []
    
    for spec in workflow_specs:
        print(f"\n=== 創建 {spec['expected_mcp_name']} ===")
        
        # 創建MCP
        create_result = creator.handle_request("create_specialized_mcp", {
            "intent_description": spec["intent_description"],
            "expected_mcp_name": spec["expected_mcp_name"],
            "intent_scope": spec["intent_scope"]
        })
        
        if create_result["status"] == "success":
            print(f"✅ 創建成功: {create_result['mcp_name']}")
            
            # 註冊MCP
            register_result = creator.handle_request("register_new_mcp", {
                "mcp_name": create_result["mcp_name"],
                "creation_record": create_result["creation_record"]
            })
            
            if register_result["status"] == "success":
                print(f"✅ 註冊成功: {register_result['mcp_name']}")
                
                # 驗證MCP
                validate_result = creator.handle_request("validate_mcp_creation", {
                    "mcp_name": create_result["mcp_name"],
                    "file_path": create_result["file_path"]
                })
                
                if validate_result["status"] == "success":
                    print(f"✅ 驗證成功: {validate_result['mcp_name']}")
                    created_mcps.append(create_result["mcp_name"])
                else:
                    print(f"❌ 驗證失敗: {validate_result}")
            else:
                print(f"❌ 註冊失敗: {register_result}")
        else:
            print(f"❌ 創建失敗: {create_result}")
    
    return created_mcps

if __name__ == "__main__":
    print("=== 批量創建工作流MCP ===")
    created = create_multiple_workflow_mcps()
    print(f"\n=== 創建完成 ===")
    print(f"成功創建 {len(created)} 個工作流MCP:")
    for mcp in created:
        print(f"  - {mcp}")

