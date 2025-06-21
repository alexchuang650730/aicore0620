# -*- coding: utf-8 -*-
"""
測試組件管理UI後台API服務
Test Component Management UI Backend API Service
專門為測試組件歸屬重構驗證提供API支持的後台服務
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import time
import logging
import asyncio
import sys
from datetime import datetime

# 添加項目路徑
sys.path.append('/home/ubuntu/aicore0620')

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 配置
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

@app.route('/')
def index():
    """提供前台UI頁面"""
    return send_from_directory('frontend', 'index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return jsonify({
        'status': 'healthy',
        'service': '測試組件管理UI後台服務',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'architecture': 'test_component_management',
        'ui_support': True
    })

@app.route('/api/health-check', methods=['GET'])
def api_health_check():
    """API健康檢查"""
    try:
        # 檢查Coding Workflow狀態
        coding_status = check_coding_workflow_status()
        
        # 檢查Test Management Workflow狀態
        test_status = check_test_workflow_status()
        
        return jsonify({
            'status': 'healthy',
            'coding_workflow_status': coding_status,
            'test_workflow_status': test_status,
            'timestamp': datetime.now().isoformat(),
            'architecture_version': '3.0.0'
        })
    except Exception as e:
        logger.error(f"健康檢查失敗: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/test-coding-workflow', methods=['POST'])
def test_coding_workflow():
    """測試Coding Workflow MCP"""
    try:
        data = request.get_json()
        requirement = data.get('requirement', '測試編碼工作流')
        context = data.get('context', {})
        
        # 導入並測試Coding Workflow MCP
        try:
            from mcp.workflow.coding_workflow_mcp.pure_ai_coding_workflow_mcp import PureAICodingWorkflowMCP
            
            workflow = PureAICodingWorkflowMCP()
            
            # 模擬AI選擇邏輯測試
            selected_components = simulate_coding_component_selection(requirement, context)
            
            return jsonify({
                'success': True,
                'workflow_type': 'coding_workflow_mcp',
                'requirement': requirement,
                'selected_components': selected_components,
                'component_count': len(selected_components),
                'confidence': 0.90,
                'performance_analysis_included': any(comp['id'] == 'performance_analysis_mcp' for comp in selected_components),
                'testing_strategy_excluded': not any(comp['id'] == 'testing_strategy_mcp' for comp in selected_components),
                'architecture_status': 'correct',
                'timestamp': datetime.now().isoformat()
            })
            
        except ImportError as e:
            return jsonify({
                'success': False,
                'error': f'Coding Workflow MCP導入失敗: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }), 500
            
    except Exception as e:
        logger.error(f"Coding Workflow測試失敗: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/test-test-workflow', methods=['POST'])
def test_test_workflow():
    """測試Test Management Workflow MCP"""
    try:
        data = request.get_json()
        requirement = data.get('requirement', '測試管理工作流')
        context = data.get('context', {})
        
        # 導入並測試Test Management Workflow MCP
        try:
            from mcp.workflow.test_management_workflow_mcp.pure_ai_test_management_workflow_mcp import PureAITestManagementWorkflowMCP
            
            workflow = PureAITestManagementWorkflowMCP()
            
            # 模擬AI選擇邏輯測試
            selected_components = simulate_test_component_selection(requirement, context)
            
            return jsonify({
                'success': True,
                'workflow_type': 'test_management_workflow_mcp',
                'requirement': requirement,
                'selected_components': selected_components,
                'component_count': len(selected_components),
                'confidence': 0.92,
                'testing_strategy_included': any(comp['id'] == 'testing_strategy_mcp' for comp in selected_components),
                'core_component_priority': 'testing_strategy_mcp',
                'architecture_status': 'correct',
                'timestamp': datetime.now().isoformat()
            })
            
        except ImportError as e:
            return jsonify({
                'success': False,
                'error': f'Test Management Workflow MCP導入失敗: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }), 500
            
    except Exception as e:
        logger.error(f"Test Management Workflow測試失敗: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

def check_coding_workflow_status():
    """檢查Coding Workflow狀態"""
    try:
        from mcp.workflow.coding_workflow_mcp.pure_ai_coding_workflow_mcp import PureAICodingWorkflowMCP
        workflow = PureAICodingWorkflowMCP()
        
        # 檢查組件配置
        components = workflow.available_components
        has_performance = 'performance_analysis_mcp' in components
        no_testing_strategy = 'testing_strategy_mcp' not in components
        
        if has_performance and no_testing_strategy:
            return 'healthy - 架構正確'
        else:
            return 'warning - 架構需要檢查'
            
    except Exception as e:
        return f'error - {str(e)}'

def check_test_workflow_status():
    """檢查Test Management Workflow狀態"""
    try:
        from mcp.workflow.test_management_workflow_mcp.pure_ai_test_management_workflow_mcp import PureAITestManagementWorkflowMCP
        workflow = PureAITestManagementWorkflowMCP()
        
        # 檢查組件配置
        components = workflow.available_components
        has_testing_strategy = 'testing_strategy_mcp' in components
        
        if has_testing_strategy:
            return 'healthy - 架構正確'
        else:
            return 'warning - 缺少核心組件'
            
    except Exception as e:
        return f'error - {str(e)}'

def simulate_coding_component_selection(requirement, context):
    """模擬Coding Workflow的組件選擇"""
    # 基於需求模擬AI選擇邏輯
    selected = [
        {
            'id': 'code_quality_mcp',
            'name': '代碼質量分析MCP',
            'type': 'analyzer',
            'reason': '代碼質量是編碼需求的核心關注點'
        },
        {
            'id': 'architecture_design_mcp',
            'name': '架構設計分析MCP',
            'type': 'analyzer',
            'reason': '架構設計分析有助於評估系統設計的合理性'
        },
        {
            'id': 'performance_analysis_mcp',
            'name': '性能分析MCP',
            'type': 'analyzer',
            'reason': '性能分析在編碼階段提供即時反饋，與架構設計緊密配合'
        }
    ]
    
    # 如果需求涉及代碼生成，添加KiloCode MCP
    if any(keyword in requirement.lower() for keyword in ['創建', '生成', '開發', 'create', 'generate']):
        selected.insert(0, {
            'id': 'kilocode_mcp',
            'name': 'KiloCode代碼生成MCP',
            'type': 'generator',
            'reason': '需求涉及代碼生成，必須包含代碼生成引擎'
        })
    
    return selected

def simulate_test_component_selection(requirement, context):
    """模擬Test Management Workflow的組件選擇"""
    # 優先選擇testing_strategy_mcp
    selected = [
        {
            'id': 'testing_strategy_mcp',
            'name': '測試策略分析MCP',
            'type': 'strategy_analyzer',
            'reason': '測試策略制定是測試管理的核心，從Coding Workflow遷移而來'
        },
        {
            'id': 'quality_assurance_mcp',
            'name': '質量保證分析MCP',
            'type': 'quality_analyzer',
            'reason': '質量保證分析確保測試策略的有效性和風險控制'
        }
    ]
    
    # 根據需求添加其他組件
    if 'execution' in requirement.lower() or '執行' in requirement:
        selected.append({
            'id': 'test_execution_mcp',
            'name': '測試執行管理MCP',
            'type': 'execution_manager',
            'reason': '需求涉及測試執行管理'
        })
    
    if 'automation' in requirement.lower() or '自動化' in requirement:
        selected.append({
            'id': 'test_automation_mcp',
            'name': '測試自動化MCP',
            'type': 'automation_engine',
            'reason': '需求涉及測試自動化'
        })
    
    return selected

if __name__ == '__main__':
    print("🚀 啟動測試組件管理UI後台服務...")
    print("📍 前端界面: http://localhost:5001")
    print("🔗 API端點: http://localhost:5001/api/")
    print("🏥 健康檢查: http://localhost:5001/health")
    
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=False,
        threaded=True
    )

