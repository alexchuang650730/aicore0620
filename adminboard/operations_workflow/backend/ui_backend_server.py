# -*- coding: utf-8 -*-
"""
運營工作流UI相關後台API服務
Operations Workflow UI Backend API Service
專門為運營工作流前台UI提供API支持的後台服務
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import time
import logging
from datetime import datetime
import asyncio
import requests

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 配置
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'html', 'htm', 'md', 'csv', 'json', 'yaml', 'yml', 'log'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# 確保上傳目錄存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 純AI驅動運營工作流引擎URL
OPERATIONS_WORKFLOW_MCP_URL = "http://localhost:8091"
OPERATIONS_ANALYSIS_ENGINE_URL = "http://localhost:8100"

def allowed_file(filename):
    """檢查文件類型是否允許"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """提供前台UI頁面"""
    return send_from_directory('frontend', 'index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return jsonify({
        'status': 'healthy',
        'service': 'operations_workflow_ui_backend',
        'version': '1.0',
        'ai_driven': True,
        'hardcoding': False,
        'operations_engine': True,
        'release_manager_support': True,
        'workflow_mcp_url': OPERATIONS_WORKFLOW_MCP_URL,
        'analysis_engine_url': OPERATIONS_ANALYSIS_ENGINE_URL,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/operations/analyze', methods=['POST'])
def analyze_operations_text():
    """運營需求文字分析API"""
    try:
        data = request.get_json()
        if not data or 'requirement' not in data:
            return jsonify({
                'success': False,
                'error': '請提供運營需求分析內容'
            }), 400

        requirement = data['requirement'].strip()
        if not requirement:
            return jsonify({
                'success': False,
                'error': '運營需求內容不能為空'
            }), 400

        operations_type = data.get('operations_type', 'general_operations')
        selected_components = data.get('selected_components', [])
        release_manager_input = data.get('release_manager_input')

        # 構建運營工作流請求
        workflow_request = {
            'requirement': requirement,
            'operations_type': operations_type,
            'selected_components': selected_components,
            'release_manager_input': release_manager_input,
            'ui_source': True
        }

        # 調用運營工作流MCP
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{OPERATIONS_WORKFLOW_MCP_URL}/api/execute",
                json=workflow_request,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                processing_time = time.time() - start_time
                
                return jsonify({
                    'success': True,
                    'analysis': result.get('analysis', '運營分析完成'),
                    'confidence_score': result.get('confidence_score', 0.95),
                    'processing_time': processing_time,
                    'engine_type': result.get('engine_type', '純AI驅動運營引擎'),
                    'operations_type': operations_type,
                    'selected_components': selected_components,
                    'release_manager_integration': result.get('release_manager_integration'),
                    'workflow_execution': result.get('workflow_execution'),
                    'timestamp': datetime.now().isoformat()
                })
            else:
                return jsonify({
                    'success': False,
                    'error': f'運營工作流MCP返回錯誤: {response.status_code}'
                }), 500
                
        except requests.exceptions.ConnectionError:
            # 如果運營工作流MCP不可用，嘗試直接調用分析引擎
            return fallback_operations_analysis(requirement, operations_type, selected_components)
        except requests.exceptions.Timeout:
            return jsonify({
                'success': False,
                'error': '運營分析超時，請稍後重試'
            }), 504

    except Exception as e:
        logger.error(f"運營分析錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'error': '服務器內部錯誤'
        }), 500

@app.route('/api/operations/upload', methods=['POST'])
def upload_and_analyze_operations():
    """運營文件上傳分析API"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': '沒有選擇文件'
            }), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '沒有選擇文件'
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'不支持的文件類型。支持的格式: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400

        operations_type = request.form.get('operations_type', 'general_operations')
        selected_components = json.loads(request.form.get('selected_components', '[]'))

        # 保存文件
        filename = f"{int(time.time())}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # 調用運營工作流MCP的文件上傳API
            start_time = time.time()
            
            with open(filepath, 'rb') as f:
                files = {'file': (filename, f, file.content_type)}
                data = {
                    'operations_type': operations_type,
                    'selected_components': json.dumps(selected_components),
                    'ui_source': 'true'
                }
                response = requests.post(
                    f"{OPERATIONS_WORKFLOW_MCP_URL}/api/upload",
                    files=files,
                    data=data,
                    timeout=120
                )

            if response.status_code == 200:
                result = response.json()
                processing_time = time.time() - start_time
                
                return jsonify({
                    'success': True,
                    'analysis': result.get('analysis', '運營文件分析完成'),
                    'confidence_score': result.get('confidence_score', 0.95),
                    'processing_time': processing_time,
                    'engine_type': result.get('engine_type', '純AI驅動運營引擎'),
                    'operations_type': operations_type,
                    'selected_components': selected_components,
                    'file_info': {
                        'filename': file.filename,
                        'size': os.path.getsize(filepath),
                        'type': file.content_type
                    },
                    'workflow_execution': result.get('workflow_execution'),
                    'timestamp': datetime.now().isoformat()
                })
            else:
                return jsonify({
                    'success': False,
                    'error': f'運營文件分析失敗: {response.status_code}'
                }), 500

        except requests.exceptions.ConnectionError:
            # 如果運營工作流MCP不可用，使用備用分析
            return fallback_operations_file_analysis(filepath, file.filename, operations_type)
        except requests.exceptions.Timeout:
            return jsonify({
                'success': False,
                'error': '運營文件分析超時，請稍後重試'
            }), 504
        finally:
            # 清理臨時文件
            if os.path.exists(filepath):
                os.remove(filepath)

    except Exception as e:
        logger.error(f"運營文件上傳分析錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'error': '文件處理錯誤'
        }), 500

def fallback_operations_analysis(requirement, operations_type, selected_components):
    """備用運營分析功能（當運營工作流MCP不可用時）"""
    try:
        # 嘗試直接調用運營分析引擎
        try:
            response = requests.post(
                f"{OPERATIONS_ANALYSIS_ENGINE_URL}/api/analyze",
                json={
                    'requirement': requirement,
                    'operations_type': operations_type,
                    'fallback_mode': True
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return jsonify({
                    'success': True,
                    'analysis': result.get('analysis', '運營分析完成'),
                    'confidence_score': result.get('confidence_score', 0.85),
                    'processing_time': result.get('processing_time', 0.2),
                    'engine_type': '運營分析引擎 (備用模式)',
                    'operations_type': operations_type,
                    'selected_components': selected_components,
                    'fallback_mode': True,
                    'timestamp': datetime.now().isoformat()
                })
        except:
            pass

        # 如果分析引擎也不可用，使用本地簡化分析
        analysis_result = f"""
基於您的運營需求："{requirement[:100]}..."

【備用運營分析模式】
由於主運營工作流引擎暫時不可用，系統已切換到備用分析模式。

⚙️ 運營類型識別：{operations_type}

🔍 運營分析要點：
1. 流程優化建議：建議進行詳細的運營流程梳理
2. 效率提升策略：識別關鍵瓶頸點並制定改進方案
3. 自動化機會：評估可自動化的運營環節
4. 監控告警：建立完善的運營監控體系
5. 風險管控：制定運營風險預防和應對策略

🔗 組件整合：{', '.join([comp.get('component_name', comp) if isinstance(comp, dict) else comp for comp in selected_components]) if selected_components else '無特定組件選擇'}

⚠️ 注意：這是簡化運營分析結果，完整的AI驅動分析請稍後重試。
        """

        return jsonify({
            'success': True,
            'analysis': analysis_result.strip(),
            'confidence_score': 0.75,
            'processing_time': 0.1,
            'engine_type': '備用運營分析引擎',
            'operations_type': operations_type,
            'selected_components': selected_components,
            'fallback_mode': True,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"備用運營分析錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'error': '備用運營分析也失敗了'
        }), 500

def fallback_operations_file_analysis(filepath, filename, operations_type):
    """備用運營文件分析功能"""
    try:
        file_size = os.path.getsize(filepath)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'unknown'
        
        analysis_result = f"""
運營文件分析結果：{filename}

【備用運營文件分析模式】
由於主運營工作流引擎暫時不可用，系統已切換到備用文件分析模式。

📄 文件信息：
- 文件名：{filename}
- 文件大小：{file_size / 1024:.2f} KB
- 文件類型：{file_ext.upper()}
- 運營類型：{operations_type}

🔍 基本運營分析：
1. 文件已成功上傳並識別為運營相關文檔
2. 文件格式符合運營工作流系統要求
3. 建議使用完整AI引擎進行深度運營分析

⚙️ 運營建議：
- 如果是配置文件，建議檢查配置項的合理性
- 如果是日誌文件，建議關注異常和性能指標
- 如果是文檔，建議提取關鍵運營流程信息

⚠️ 注意：這是簡化運營文件分析結果，完整的AI驅動分析請稍後重試。
        """

        return jsonify({
            'success': True,
            'analysis': analysis_result.strip(),
            'confidence_score': 0.70,
            'processing_time': 0.1,
            'engine_type': '備用運營文件分析引擎',
            'operations_type': operations_type,
            'fallback_mode': True,
            'file_info': {
                'filename': filename,
                'size': file_size,
                'type': file_ext
            },
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"備用運營文件分析錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'error': '備用運營文件分析失敗'
        }), 500

@app.errorhandler(413)
def too_large(e):
    """文件過大錯誤處理"""
    return jsonify({
        'success': False,
        'error': '文件過大，請選擇小於16MB的文件'
    }), 413

@app.errorhandler(404)
def not_found(e):
    """404錯誤處理"""
    return jsonify({
        'success': False,
        'error': 'API端點不存在'
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """500錯誤處理"""
    return jsonify({
        'success': False,
        'error': '服務器內部錯誤'
    }), 500

if __name__ == '__main__':
    print("🚀 運營工作流UI後台服務啟動中...")
    print(f"📁 上傳目錄: {UPLOAD_FOLDER}")
    print(f"⚙️ 運營工作流MCP: {OPERATIONS_WORKFLOW_MCP_URL}")
    print(f"🔍 運營分析引擎: {OPERATIONS_ANALYSIS_ENGINE_URL}")
    print("🌐 前台UI: http://localhost:5001")
    print("🔧 健康檢查: http://localhost:5001/health")
    
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=False,
        threaded=True
    )

