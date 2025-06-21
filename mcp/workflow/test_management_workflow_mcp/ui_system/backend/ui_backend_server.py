# -*- coding: utf-8 -*-
"""
AICore0620 七大工作流測試系統後端服務
整合現有測試架構，提供統一的測試執行界面

Author: AICore0620 Team
Date: 2025-06-21
Version: 2.0.0
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import json
import subprocess
import yaml
from datetime import datetime
from pathlib import Path
import asyncio
import importlib.util

# 添加項目路徑
sys.path.append('/opt/aiengine')
sys.path.append('/opt/aiengine/mcp')
sys.path.append('/home/ubuntu/aicore0620')
sys.path.append('/home/ubuntu/aicore0620/mcp')

app = Flask(__name__)
CORS(app)

# 七大工作流配置
WORKFLOWS = {
    'coding_workflow_mcp': {
        'name': '編碼工作流',
        'port': 8888,
        'path': 'mcp/workflow/coding_workflow_mcp',
        'description': '代碼生成、性能分析、架構設計'
    },
    'requirements_analysis_mcp': {
        'name': '需求分析工作流',
        'port': 8100,
        'path': 'mcp/workflow/requirements_analysis_mcp',
        'description': '需求分析、業務邏輯、用戶故事'
    },
    'operations_workflow_mcp': {
        'name': '運營工作流',
        'port': 8091,
        'path': 'mcp/workflow/operations_workflow_mcp',
        'description': '運營自動化、監控、部署'
    },
    'release_manager_mcp': {
        'name': '發布管理工作流',
        'port': 8092,
        'path': 'mcp/workflow/release_manager_mcp',
        'description': '版本管理、發布流程、回滾策略'
    },
    'architecture_design_mcp': {
        'name': '架構設計工作流',
        'port': 8093,
        'path': 'mcp/workflow/architecture_design_mcp',
        'description': '系統架構、設計模式、技術選型'
    },
    'developer_flow_mcp': {
        'name': '開發者工作流',
        'port': 8094,
        'path': 'mcp/workflow/developer_flow_mcp',
        'description': '開發流程、代碼審查、協作管理'
    },
    'test_management_workflow_mcp': {
        'name': '測試管理工作流',
        'port': 8321,
        'path': 'mcp/workflow/test_management_workflow_mcp',
        'description': '測試策略、質量保證、測試執行'
    }
}

@app.route('/')
def index():
    """提供前台UI頁面"""
    try:
        return send_file('frontend/index.html')
    except Exception as e:
        # 如果文件不存在，直接返回HTML內容
        with open('frontend/index.html', 'r', encoding='utf-8') as f:
            return f.read()

@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return jsonify({
        'status': 'healthy',
        'service': 'AICore0620 七大工作流測試系統',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat(),
        'workflows_count': len(WORKFLOWS),
        'supported_workflows': list(WORKFLOWS.keys())
    })

@app.route('/api/health-check', methods=['GET'])
def api_health_check():
    """API健康檢查"""
    workflow_status = {}
    
    for workflow_id, config in WORKFLOWS.items():
        try:
            # 檢查工作流目錄是否存在
            workflow_path = Path('/home/ubuntu/aicore0620') / config['path']
            if workflow_path.exists():
                # 檢查測試目錄
                unit_tests = (workflow_path / 'unit_tests').exists()
                integration_tests = (workflow_path / 'integration_tests').exists()
                testcases = (workflow_path / 'testcases').exists()
                
                workflow_status[workflow_id] = {
                    'status': 'available',
                    'unit_tests': unit_tests,
                    'integration_tests': integration_tests,
                    'testcases': testcases,
                    'path': str(workflow_path)
                }
            else:
                workflow_status[workflow_id] = {
                    'status': 'not_found',
                    'path': str(workflow_path)
                }
        except Exception as e:
            workflow_status[workflow_id] = {
                'status': 'error',
                'error': str(e)
            }
    
    return jsonify({
        'status': 'healthy',
        'system_version': '2.0.0',
        'timestamp': datetime.now().isoformat(),
        'workflows': workflow_status
    })

@app.route('/api/workflows', methods=['GET'])
def get_workflows():
    """獲取所有可用工作流"""
    return jsonify({
        'success': True,
        'workflows': WORKFLOWS,
        'count': len(WORKFLOWS)
    })

@app.route('/api/workflow-test', methods=['POST'])
def workflow_test():
    """統一的工作流測試端點"""
    try:
        data = request.get_json()
        workflow_id = data.get('workflow_id')
        test_type = data.get('test_type', 'unit')  # unit 或 integration
        description = data.get('description', '')
        extra_params = data.get('extra_params', {})
        
        if not workflow_id:
            return jsonify({'error': '請指定工作流ID'}), 400
            
        if workflow_id not in WORKFLOWS:
            return jsonify({'error': f'不支持的工作流: {workflow_id}'}), 400
        
        workflow_config = WORKFLOWS[workflow_id]
        
        # 執行測試
        result = execute_workflow_test(workflow_id, test_type, description, extra_params)
        
        return jsonify({
            'success': True,
            'workflow_id': workflow_id,
            'workflow_name': workflow_config['name'],
            'test_type': test_type,
            'description': description,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/generate-curl', methods=['POST'])
def generate_curl():
    """生成curl命令"""
    try:
        data = request.get_json()
        workflow_id = data.get('workflow_id')
        test_type = data.get('test_type', 'unit')
        description = data.get('description', '')
        extra_params = data.get('extra_params', {})
        
        if not workflow_id:
            return jsonify({'error': '請指定工作流ID'}), 400
        
        # 構建curl命令
        curl_data = {
            'workflow_id': workflow_id,
            'test_type': test_type,
            'description': description,
            'extra_params': extra_params
        }
        
        curl_command = f"""curl -X POST http://localhost:5001/api/workflow-test \\
  -H "Content-Type: application/json" \\
  -d '{json.dumps(curl_data, ensure_ascii=False)}'"""
        
        return jsonify({
            'success': True,
            'curl_command': curl_command,
            'parameters': curl_data,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/testcases/<workflow_id>', methods=['GET'])
def get_testcases(workflow_id):
    """獲取指定工作流的測試用例"""
    try:
        if workflow_id not in WORKFLOWS:
            return jsonify({'error': f'不支持的工作流: {workflow_id}'}), 400
        
        workflow_config = WORKFLOWS[workflow_id]
        workflow_path = Path(workflow_config['path'])
        testcases_path = workflow_path / 'testcases'
        
        testcases = {}
        
        if testcases_path.exists():
            # 讀取測試配置
            config_file = testcases_path / 'testcase_config.yaml'
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    testcases['config'] = yaml.safe_load(f)
            
            # 讀取測試模板
            for template_file in testcases_path.glob('*.md'):
                with open(template_file, 'r', encoding='utf-8') as f:
                    testcases[template_file.stem] = f.read()
        
        return jsonify({
            'success': True,
            'workflow_id': workflow_id,
            'testcases': testcases,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

def execute_workflow_test(workflow_id, test_type, description, extra_params):
    """執行工作流測試"""
    try:
        workflow_config = WORKFLOWS[workflow_id]
        # 修正路徑：使用絕對路徑
        workflow_path = Path('/home/ubuntu/aicore0620') / workflow_config['path']
        
        if test_type == 'unit':
            return execute_unit_tests(workflow_path, workflow_id)
        elif test_type == 'integration':
            return execute_integration_tests(workflow_path, workflow_id)
        else:
            return {
                'status': 'error',
                'message': f'不支持的測試類型: {test_type}'
            }
            
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

def execute_unit_tests(workflow_path, workflow_id):
    """執行單元測試"""
    try:
        unit_tests_path = workflow_path / 'unit_tests'
        
        print(f"🔍 檢查路徑: {unit_tests_path}")  # 調試信息
        
        if not unit_tests_path.exists():
            return {
                'status': 'warning',
                'message': f'工作流 {workflow_id} 沒有單元測試目錄',
                'path': str(unit_tests_path),
                'debug_info': f'檢查路徑: {unit_tests_path}, 存在: {unit_tests_path.exists()}'
            }
        
        # 查找測試文件
        test_files = list(unit_tests_path.glob('test_*.py'))
        
        if not test_files:
            return {
                'status': 'warning',
                'message': f'工作流 {workflow_id} 沒有找到測試文件',
                'path': str(unit_tests_path),
                'files_found': [str(f) for f in unit_tests_path.glob('*.py')]
            }
        
        # 直接執行unittest而不是pytest
        result = run_unittest(unit_tests_path, workflow_id)
        
        return {
            'status': 'success',
            'test_type': 'unit_tests',
            'test_files': [str(f.name) for f in test_files],
            'result': result,
            'path': str(unit_tests_path)
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'執行單元測試失敗: {str(e)}'
        }

def execute_integration_tests(workflow_path, workflow_id):
    """執行集成測試"""
    try:
        integration_tests_path = workflow_path / 'integration_tests'
        
        if not integration_tests_path.exists():
            return {
                'status': 'warning',
                'message': f'工作流 {workflow_id} 沒有集成測試目錄',
                'path': str(integration_tests_path)
            }
        
        # 查找測試文件
        test_files = list(integration_tests_path.glob('test_*.py'))
        
        if not test_files:
            return {
                'status': 'warning',
                'message': f'工作流 {workflow_id} 沒有找到集成測試文件',
                'path': str(integration_tests_path)
            }
        
        # 執行pytest
        result = run_pytest(integration_tests_path)
        
        return {
            'status': 'success',
            'test_type': 'integration_tests',
            'test_files': [str(f.name) for f in test_files],
            'result': result,
            'path': str(integration_tests_path)
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'執行集成測試失敗: {str(e)}'
        }

def run_unittest(test_path, workflow_id):
    """運行unittest測試"""
    try:
        # 查找主要的測試文件
        test_file = test_path / f'test_{workflow_id}.py'
        
        if not test_file.exists():
            # 如果沒有找到主測試文件，查找其他test_*.py文件
            test_files = list(test_path.glob('test_*.py'))
            if test_files:
                test_file = test_files[0]  # 使用第一個找到的測試文件
            else:
                return {
                    'returncode': -1,
                    'stdout': '',
                    'stderr': f'沒有找到測試文件: {test_file}',
                    'success': False
                }
        
        # 使用subprocess運行unittest
        cmd = ['python3', '-m', 'unittest', f'test_{workflow_id}.py', '-v']
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,  # 60秒超時
            cwd=str(test_path)  # 在測試目錄中運行
        )
        
        return {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'success': result.returncode == 0,
            'test_file': str(test_file)
        }
        
    except subprocess.TimeoutExpired:
        return {
            'returncode': -1,
            'stdout': '',
            'stderr': '測試執行超時',
            'success': False
        }
    except Exception as e:
        return {
            'returncode': -1,
            'stdout': '',
            'stderr': str(e),
            'success': False
        }

def run_pytest(test_path):
    """運行pytest測試"""
    try:
        # 使用subprocess運行pytest
        cmd = ['python', '-m', 'pytest', str(test_path), '-v', '--tb=short']
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,  # 60秒超時
            cwd='/opt/aiengine'
        )
        
        return {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'success': result.returncode == 0
        }
        
    except subprocess.TimeoutExpired:
        return {
            'returncode': -1,
            'stdout': '',
            'stderr': '測試執行超時',
            'success': False
        }
    except Exception as e:
        return {
            'returncode': -1,
            'stdout': '',
            'stderr': str(e),
            'success': False
        }

if __name__ == '__main__':
    print('🚀 啟動AICore0620七大工作流測試系統...')
    print('📍 前端界面: http://localhost:5001')
    print('🔗 API端點: http://localhost:5001/api/')
    print('🏥 健康檢查: http://localhost:5001/health')
    print(f'📋 支持的工作流: {len(WORKFLOWS)}個')
    
    for workflow_id, config in WORKFLOWS.items():
        print(f'   - {config["name"]} ({workflow_id})')
    
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)

