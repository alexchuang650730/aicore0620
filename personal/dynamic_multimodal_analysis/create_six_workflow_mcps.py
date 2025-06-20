#!/usr/bin/env python3
"""
創建六大標準工作流MCP
"""

import sys
import os
import asyncio
sys.path.append('/home/ubuntu/enterprise_deployment')

from mcp.coordinator.dynamic_mcp_creator_mcp import DynamicMCPCreatorMCP

async def create_six_standard_workflow_mcps():
    """創建六大標準工作流MCP"""
    creator = DynamicMCPCreatorMCP()
    
    # 六大標準工作流MCP規格
    workflow_specs = [
        {
            "intent_description": "需求分析和業務需求整理",
            "expected_mcp_name": "requirements_analysis_workflow_mcp",
            "intent_scope": {
                "primary_scope": "需求分析",
                "secondary_scopes": ["需求收集", "業務分析", "用戶故事", "需求文檔"]
            }
        },
        {
            "intent_description": "系統架構設計和技術選型",
            "expected_mcp_name": "architecture_design_workflow_mcp", 
            "intent_scope": {
                "primary_scope": "架構設計",
                "secondary_scopes": ["技術選型", "系統設計", "架構規劃", "設計文檔"]
            }
        },
        {
            "intent_description": "編碼實現和程式開發",
            "expected_mcp_name": "coding_implementation_workflow_mcp",
            "intent_scope": {
                "primary_scope": "編碼實現",
                "secondary_scopes": ["程式開發", "代碼編寫", "功能實現", "代碼審查"]
            }
        },
        {
            "intent_description": "測試驗證和品質保證",
            "expected_mcp_name": "testing_validation_workflow_mcp",
            "intent_scope": {
                "primary_scope": "測試驗證",
                "secondary_scopes": ["功能測試", "性能測試", "安全測試", "品質保證"]
            }
        },
        {
            "intent_description": "部署運維和系統管理",
            "expected_mcp_name": "deployment_operations_workflow_mcp",
            "intent_scope": {
                "primary_scope": "部署運維",
                "secondary_scopes": ["系統部署", "運維管理", "監控告警", "性能優化"]
            }
        },
        {
            "intent_description": "維護支援和技術服務",
            "expected_mcp_name": "maintenance_support_workflow_mcp",
            "intent_scope": {
                "primary_scope": "維護支援",
                "secondary_scopes": ["系統維護", "技術支援", "問題排除", "文檔更新"]
            }
        }
    ]
    
    created_mcps = []
    
    for spec in workflow_specs:
        print(f"\n=== 創建 {spec['expected_mcp_name']} ===")
        
        try:
            # 創建MCP
            create_result = await creator.handle_request("create_specialized_mcp", {
                "intent_description": spec["intent_description"],
                "expected_mcp_name": spec["expected_mcp_name"],
                "intent_scope": spec["intent_scope"]
            })
            
            if create_result["status"] == "success":
                print(f"✅ 創建成功: {create_result['mcp_name']}")
                
                # 註冊MCP
                register_result = await creator.handle_request("register_new_mcp", {
                    "mcp_name": create_result["mcp_name"],
                    "creation_record": create_result["creation_record"]
                })
                
                if register_result["status"] == "success":
                    print(f"✅ 註冊成功: {register_result['mcp_name']}")
                    
                    # 驗證MCP
                    validate_result = await creator.handle_request("validate_mcp_creation", {
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
                
        except Exception as e:
            print(f"❌ 處理 {spec['expected_mcp_name']} 時發生錯誤: {e}")
    
    return created_mcps

if __name__ == "__main__":
    print("=== 創建六大標準工作流MCP ===")
    created = asyncio.run(create_six_standard_workflow_mcps())
    print(f"\n=== 創建完成 ===")
    print(f"成功創建 {len(created)} 個標準工作流MCP:")
    for mcp in created:
        print(f"  - {mcp}")

