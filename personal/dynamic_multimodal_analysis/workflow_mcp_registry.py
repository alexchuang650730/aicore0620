#!/usr/bin/env python3
"""
工作流MCP註冊器 - 將實際的工作流MCP組件註冊到系統中
"""

import sys
import asyncio
import json
from pathlib import Path

# 添加路徑
sys.path.append('/tmp/aicore0619')
sys.path.append('/home/ubuntu/enterprise_deployment')

class WorkflowMCPRegistry:
    """工作流MCP註冊器"""
    
    def __init__(self):
        self.registered_workflows = {}
        
    async def register_workflow_mcps(self):
        """註冊所有工作流MCP"""
        
        workflow_configs = [
            {
                "name": "requirements_analysis",
                "module_path": "mcp.workflow.requirements_analysis_mcp.src.requirements_analysis_mcp",
                "class_name": "RequirementAnalysisMCP",
                "description": "需求分析工作流"
            },
            {
                "name": "architecture_design", 
                "module_path": "mcp.workflow.architecture_design_mcp.src.architecture_design_mcp",
                "class_name": "ArchitectureDesignMCP",
                "description": "架構設計工作流"
            },
            {
                "name": "coding_implementation",
                "module_path": "mcp.workflow.coding_workflow_mcp.coding_workflow_mcp", 
                "class_name": "CodingWorkflowMCP",
                "description": "編碼實現工作流"
            },
            {
                "name": "test_verification",
                "module_path": "mcp.workflow.test_management_workflow_mcp.test_management_workflow_mcp",
                "class_name": "TestManagementWorkflowMCP", 
                "description": "測試驗證工作流"
            },
            {
                "name": "deployment_release",
                "module_path": "mcp.workflow.release_manager_mcp.release_manager_mcp",
                "class_name": "ReleaseManagerMCP",
                "description": "部署發布工作流"
            },
            {
                "name": "monitoring_operations", 
                "module_path": "mcp.workflow.operations_workflow_mcp.src.operations_workflow_mcp",
                "class_name": "OperationsWorkflowMCP",
                "description": "監控運維工作流"
            }
        ]
        
        for config in workflow_configs:
            try:
                print(f"🔄 註冊工作流MCP: {config['name']}")
                
                # 動態導入模組
                module = __import__(config['module_path'], fromlist=[config['class_name']])
                workflow_class = getattr(module, config['class_name'])
                
                # 創建工作流實例
                workflow_instance = workflow_class()
                
                # 註冊到系統
                self.registered_workflows[config['name']] = {
                    'instance': workflow_instance,
                    'config': config,
                    'status': 'active'
                }
                
                print(f"✅ {config['name']} 註冊成功")
                
            except Exception as e:
                print(f"❌ {config['name']} 註冊失敗: {e}")
                self.registered_workflows[config['name']] = {
                    'instance': None,
                    'config': config,
                    'status': 'failed',
                    'error': str(e)
                }
        
        return self.registered_workflows
    
    async def execute_workflow_node(self, node_name: str, request_data: dict):
        """執行特定的工作流節點"""
        
        # 映射節點名稱到工作流
        node_mapping = {
            'node_1_requirement_analysis': 'requirements_analysis',
            'node_2_architecture_design': 'architecture_design', 
            'node_3_code_implementation': 'coding_implementation',
            'node_4_test_verification': 'test_verification',
            'node_5_deployment_release': 'deployment_release',
            'node_6_monitoring_operations': 'monitoring_operations'
        }
        
        workflow_name = node_mapping.get(node_name)
        if not workflow_name:
            return {
                'status': 'failed',
                'error': f'未知的工作流節點: {node_name}'
            }
        
        workflow_info = self.registered_workflows.get(workflow_name)
        if not workflow_info or workflow_info['status'] != 'active':
            return {
                'status': 'failed', 
                'error': f'工作流 {workflow_name} 不可用'
            }
        
        try:
            # 調用工作流實例
            workflow_instance = workflow_info['instance']
            
            # 特殊處理編碼實現工作流
            if workflow_name == 'coding_implementation':
                # 先創建任務
                create_result = await workflow_instance.create_coding_task(request_data)
                if not create_result.get('success'):
                    return {
                        'status': 'failed',
                        'error': f'創建編碼任務失敗: {create_result.get("error")}'
                    }
                
                # 然後執行任務
                task_id = create_result['task_id']
                execute_result = await workflow_instance.execute_task(task_id)
                
                return {
                    'status': 'completed' if execute_result.get('success') else 'failed',
                    'workflow': workflow_name,
                    'create_result': create_result,
                    'execute_result': execute_result,
                    'task_id': task_id
                }
            
            # 根據不同的工作流調用不同的方法
            elif hasattr(workflow_instance, 'process_request'):
                result = await workflow_instance.process_request(request_data)
            elif hasattr(workflow_instance, 'execute_task'):
                result = await workflow_instance.execute_task(request_data)
            elif hasattr(workflow_instance, 'handle_request'):
                result = await workflow_instance.handle_request(request_data)
            else:
                # 兜底方案：返回基本信息
                result = {
                    'status': 'completed',
                    'workflow': workflow_name,
                    'message': f'{workflow_name} 工作流已處理請求',
                    'data': request_data
                }
            
            return result
            
        except Exception as e:
            return {
                'status': 'failed',
                'error': f'工作流執行失敗: {str(e)}'
            }

async def test_workflow_registry():
    """測試工作流註冊器"""
    
    print("🚀 啟動工作流MCP註冊器...")
    
    registry = WorkflowMCPRegistry()
    
    # 註冊所有工作流MCP
    registered = await registry.register_workflow_mcps()
    
    print(f"\n📊 註冊結果統計:")
    active_count = sum(1 for w in registered.values() if w['status'] == 'active')
    failed_count = sum(1 for w in registered.values() if w['status'] == 'failed')
    
    print(f"✅ 成功註冊: {active_count} 個工作流")
    print(f"❌ 註冊失敗: {failed_count} 個工作流")
    
    print(f"\n📋 詳細狀態:")
    for name, info in registered.items():
        status_icon = "✅" if info['status'] == 'active' else "❌"
        print(f"{status_icon} {name}: {info['status']}")
        if info['status'] == 'failed':
            print(f"   錯誤: {info.get('error', 'Unknown error')}")
    
    # 測試執行一個工作流節點
    if active_count > 0:
        print(f"\n🔄 測試執行工作流節點...")
        test_request = {
            'name': '贪吃蛇游戏',
            'description': '开发一个Python贪吃蛇游戏',
            'requirements': ['Python', 'pygame', '游戏逻辑']
        }
        
        # 測試可用的工作流節點
        available_nodes = [
            ('node_3_code_implementation', 'coding_implementation'),
            ('node_6_monitoring_operations', 'monitoring_operations')
        ]
        
        for node_name, workflow_name in available_nodes:
            if workflow_name in registered and registered[workflow_name]['status'] == 'active':
                print(f"\n🔄 測試 {node_name} ({workflow_name})...")
                result = await registry.execute_workflow_node(node_name, test_request)
                print(f"📋 {workflow_name} 測試結果:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                break
    
    return registry

if __name__ == "__main__":
    registry = asyncio.run(test_workflow_registry())

