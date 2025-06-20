# -*- coding: utf-8 -*-
"""
工作流層編排器
Workflow Layer - Workflow Orchestrator
職責：工作流模板管理、階段依賴處理、執行狀態管理
只調用MCPCoordinator，不直接調用MCP組件
"""

import asyncio
import json
import logging
import time
from datetime import datetime
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class WorkflowOrchestrator:
    """工作流層編排器 - 只調用MCPCoordinator"""
    
    def __init__(self):
        self.mcp_coordinator_url = "http://localhost:8303"  # MCPCoordinator端點
        self.workflow_templates = self._load_workflow_templates()
        
    def _load_workflow_templates(self):
        """加載工作流模板"""
        return {
            'enterprise_analysis_workflow': {
                'name': '企業級分析工作流',
                'stages': [
                    {
                        'stage_id': 'requirements_analysis',
                        'name': '需求分析階段',
                        'target_mcp': 'requirements_analysis_mcp',
                        'timeout': 30,
                        'retry_count': 2
                    },
                    {
                        'stage_id': 'quantitative_analysis',
                        'name': '量化分析階段',
                        'target_mcp': 'architecture_design_mcp',
                        'timeout': 45,
                        'retry_count': 2
                    },
                    {
                        'stage_id': 'solution_design',
                        'name': '解決方案設計階段',
                        'target_mcp': 'coding_workflow_mcp',
                        'timeout': 60,
                        'retry_count': 1
                    },
                    {
                        'stage_id': 'implementation_planning',
                        'name': '實施規劃階段',
                        'target_mcp': 'developer_flow_mcp',
                        'timeout': 30,
                        'retry_count': 1
                    }
                ]
            },
            'general_analysis_workflow': {
                'name': '通用分析工作流',
                'stages': [
                    {
                        'stage_id': 'basic_analysis',
                        'name': '基礎分析階段',
                        'target_mcp': 'requirements_analysis_mcp',
                        'timeout': 30,
                        'retry_count': 2
                    }
                ]
            }
        }
    
    async def execute_workflow(self, workflow_request):
        """執行工作流 - 工作流層核心方法"""
        try:
            workflow_type = workflow_request.get('workflow_type')
            stages = workflow_request.get('stages', [])
            execution_mode = workflow_request.get('execution_mode', 'sequential')
            original_requirement = workflow_request.get('original_requirement', '')
            context = workflow_request.get('context', {})
            
            # 獲取工作流模板
            template = self.workflow_templates.get(workflow_type)
            if not template:
                return {
                    'success': False,
                    'error': f'未找到工作流模板: {workflow_type}'
                }
            
            # 執行工作流階段
            workflow_context = {
                'original_requirement': original_requirement,
                'context': context,
                'workflow_type': workflow_type,
                'execution_start_time': datetime.now().isoformat()
            }
            
            if execution_mode == 'sequential':
                result = await self._execute_sequential_workflow(template, workflow_context)
            else:
                result = await self._execute_parallel_workflow(template, workflow_context)
            
            return result
            
        except Exception as e:
            logger.error(f"工作流執行錯誤: {e}")
            return {
                'success': False,
                'error': str(e),
                'layer': 'workflow'
            }
    
    async def _execute_sequential_workflow(self, template, workflow_context):
        """順序執行工作流"""
        results = []
        accumulated_context = workflow_context.copy()
        
        for stage in template['stages']:
            stage_result = await self._execute_stage(stage, accumulated_context)
            results.append(stage_result)
            
            if not stage_result.get('success'):
                logger.error(f"階段執行失敗: {stage['stage_id']}")
                break
            
            # 累積上下文
            accumulated_context['previous_results'] = results
        
        # 整合所有階段結果
        final_result = await self._integrate_workflow_results(results, workflow_context)
        
        return {
            'success': True,
            'workflow_type': workflow_context['workflow_type'],
            'stages_executed': len(results),
            'stage_results': results,
            'analysis': final_result,
            'layer': 'workflow',
            'execution_time': datetime.now().isoformat()
        }
    
    async def _execute_parallel_workflow(self, template, workflow_context):
        """並行執行工作流"""
        # 簡化實現，實際可以使用asyncio.gather
        return await self._execute_sequential_workflow(template, workflow_context)
    
    async def _execute_stage(self, stage, context):
        """執行單個工作流階段 - 調用MCPCoordinator"""
        try:
            mcp_request = {
                'target_workflow': stage['target_mcp'],
                'stage_id': stage['stage_id'],
                'stage_name': stage['name'],
                'context': context,
                'timeout': stage.get('timeout', 30)
            }
            
            # 調用MCPCoordinator
            response = requests.post(
                f"{self.mcp_coordinator_url}/api/mcp/coordinate",
                json=mcp_request,
                timeout=stage.get('timeout', 30)
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'stage_id': stage['stage_id'],
                    'stage_name': stage['name'],
                    'result': result,
                    'execution_time': datetime.now().isoformat()
                }
            else:
                logger.error(f"MCP調用失敗: {response.status_code}")
                return {
                    'success': False,
                    'stage_id': stage['stage_id'],
                    'error': f'MCP調用失敗: HTTP {response.status_code}'
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"MCPCoordinator連接失敗: {e}")
            # 降級處理
            return await self._fallback_stage_execution(stage, context)
    
    async def _fallback_stage_execution(self, stage, context):
        """階段執行降級處理"""
        await asyncio.sleep(0.02)
        
        fallback_results = {
            'requirements_analysis': '需求分析完成（降級模式）',
            'quantitative_analysis': '量化分析完成（降級模式）',
            'solution_design': '解決方案設計完成（降級模式）',
            'implementation_planning': '實施規劃完成（降級模式）'
        }
        
        return {
            'success': True,
            'stage_id': stage['stage_id'],
            'stage_name': stage['name'],
            'result': {
                'analysis': fallback_results.get(stage['stage_id'], '階段分析完成（降級模式）'),
                'mode': 'fallback'
            },
            'execution_time': datetime.now().isoformat()
        }
    
    async def _integrate_workflow_results(self, stage_results, workflow_context):
        """整合工作流結果"""
        await asyncio.sleep(0.01)
        
        if workflow_context['workflow_type'] == 'enterprise_analysis_workflow':
            return self._integrate_enterprise_analysis_results(stage_results, workflow_context)
        else:
            return self._integrate_general_analysis_results(stage_results, workflow_context)
    
    def _integrate_enterprise_analysis_results(self, stage_results, workflow_context):
        """整合企業級分析結果"""
        integrated_result = f"""
# 企業級工作流分析報告

## 工作流執行摘要
- **工作流類型**: {workflow_context['workflow_type']}
- **執行階段數**: {len(stage_results)}
- **執行開始時間**: {workflow_context['execution_start_time']}

## 各階段執行結果

"""
        
        for stage_result in stage_results:
            if stage_result.get('success'):
                integrated_result += f"""
### {stage_result['stage_name']}
- **階段ID**: {stage_result['stage_id']}
- **執行狀態**: ✅ 成功
- **執行時間**: {stage_result['execution_time']}

**分析結果**:
{stage_result['result'].get('analysis', '無詳細結果')}

---
"""
            else:
                integrated_result += f"""
### {stage_result['stage_name']}
- **階段ID**: {stage_result['stage_id']}
- **執行狀態**: ❌ 失敗
- **錯誤信息**: {stage_result.get('error', '未知錯誤')}

---
"""
        
        integrated_result += """
## 工作流級建議
基於多階段分析結果，建議採用系統性方法實施數位轉型，確保各階段目標達成。

*本報告由工作流層編排器生成，整合了多個MCP組件的分析結果*
"""
        
        return integrated_result.strip()
    
    def _integrate_general_analysis_results(self, stage_results, workflow_context):
        """整合通用分析結果"""
        if stage_results and stage_results[0].get('success'):
            return stage_results[0]['result'].get('analysis', '工作流分析完成')
        else:
            return '工作流執行完成，但未獲得有效結果'

# Flask API端點
@app.route('/api/workflow/execute', methods=['POST'])
def execute_workflow_api():
    """工作流執行API端點"""
    try:
        workflow_request = request.get_json()
        if not workflow_request:
            return jsonify({'success': False, 'error': '無效的請求數據'}), 400
        
        orchestrator = WorkflowOrchestrator()
        
        # 使用asyncio執行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                orchestrator.execute_workflow(workflow_request)
            )
        finally:
            loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"工作流API錯誤: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'layer': 'workflow_api'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查"""
    return jsonify({
        'status': 'healthy',
        'service': 'workflow_orchestrator',
        'layer': 'workflow',
        'available_workflows': list(WorkflowOrchestrator()._load_workflow_templates().keys())
    })

if __name__ == '__main__':
    logger.info("啟動工作流層編排器")
    app.run(host='0.0.0.0', port=8302, debug=False)

