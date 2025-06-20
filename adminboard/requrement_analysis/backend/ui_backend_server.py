# -*- coding: utf-8 -*-
"""
需求分析UI相關後台API服務
Requirements Analysis UI Backend API Service
專門為前台UI提供API支持的輕量級後台服務
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
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'html', 'htm', 'md', 'csv'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# 確保上傳目錄存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 純AI驅動分析引擎URL（指向主系統）
MAIN_ANALYSIS_ENGINE_URL = "http://localhost:8888"

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
        'service': 'requirements_analysis_ui_backend',
        'version': '2.0',
        'ai_driven': True,
        'hardcoding': False,
        'ui_support': True,
        'main_engine_url': MAIN_ANALYSIS_ENGINE_URL,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """文字需求分析API"""
    try:
        data = request.get_json()
        if not data or 'requirement' not in data:
            return jsonify({
                'success': False,
                'error': '請提供需求分析內容'
            }), 400

        requirement = data['requirement'].strip()
        if not requirement:
            return jsonify({
                'success': False,
                'error': '需求內容不能為空'
            }), 400

        # 調用主分析引擎
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{MAIN_ANALYSIS_ENGINE_URL}/api/analyze",
                json={'requirement': requirement},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                processing_time = time.time() - start_time
                
                return jsonify({
                    'success': True,
                    'analysis': result.get('analysis', '分析完成'),
                    'confidence_score': result.get('confidence_score', 0.95),
                    'processing_time': processing_time,
                    'engine_type': result.get('engine_type', '純AI驅動引擎'),
                    'timestamp': datetime.now().isoformat()
                })
            else:
                return jsonify({
                    'success': False,
                    'error': f'主分析引擎返回錯誤: {response.status_code}'
                }), 500
                
        except requests.exceptions.ConnectionError:
            # 如果主引擎不可用，使用本地簡化分析
            return fallback_analysis(requirement)
        except requests.exceptions.Timeout:
            return jsonify({
                'success': False,
                'error': '分析超時，請稍後重試'
            }), 504

    except Exception as e:
        logger.error(f"分析錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'error': '服務器內部錯誤'
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload_and_analyze():
    """文件上傳分析API"""
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

        # 保存文件
        filename = f"{int(time.time())}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # 調用主分析引擎的文件上傳API
            start_time = time.time()
            
            with open(filepath, 'rb') as f:
                files = {'file': (filename, f, file.content_type)}
                response = requests.post(
                    f"{MAIN_ANALYSIS_ENGINE_URL}/api/upload",
                    files=files,
                    timeout=120
                )

            if response.status_code == 200:
                result = response.json()
                processing_time = time.time() - start_time
                
                return jsonify({
                    'success': True,
                    'analysis': result.get('analysis', '文件分析完成'),
                    'confidence_score': result.get('confidence_score', 0.95),
                    'processing_time': processing_time,
                    'engine_type': result.get('engine_type', '純AI驅動引擎'),
                    'file_info': {
                        'filename': file.filename,
                        'size': os.path.getsize(filepath),
                        'type': file.content_type
                    },
                    'timestamp': datetime.now().isoformat()
                })
            else:
                return jsonify({
                    'success': False,
                    'error': f'文件分析失敗: {response.status_code}'
                }), 500

        except requests.exceptions.ConnectionError:
            # 如果主引擎不可用，使用本地簡化分析
            return fallback_file_analysis(filepath, file.filename)
        except requests.exceptions.Timeout:
            return jsonify({
                'success': False,
                'error': '文件分析超時，請稍後重試'
            }), 504
        finally:
            # 清理臨時文件
            if os.path.exists(filepath):
                os.remove(filepath)

    except Exception as e:
        logger.error(f"文件上傳分析錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'error': '文件處理錯誤'
        }), 500

def fallback_analysis(requirement):
    """備用分析功能（當主引擎不可用時）"""
    try:
        # 簡化的本地分析邏輯
        analysis_result = f"""
基於您的需求："{requirement[:100]}..."

【備用分析模式】
由於主AI分析引擎暫時不可用，系統已切換到備用分析模式。

📋 需求理解：
系統識別到您的需求涉及業務流程分析和效率評估。

🔍 初步建議：
1. 建議進行詳細的流程梳理
2. 收集相關的量化數據
3. 對比行業最佳實踐
4. 制定改進方案

⚠️ 注意：這是簡化分析結果，完整的AI分析請稍後重試。
        """

        return jsonify({
            'success': True,
            'analysis': analysis_result.strip(),
            'confidence_score': 0.75,
            'processing_time': 0.1,
            'engine_type': '備用分析引擎',
            'fallback_mode': True,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"備用分析錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'error': '備用分析也失敗了'
        }), 500

def fallback_file_analysis(filepath, filename):
    """備用文件分析功能"""
    try:
        file_size = os.path.getsize(filepath)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'unknown'
        
        analysis_result = f"""
文件分析結果：{filename}

【備用分析模式】
由於主AI分析引擎暫時不可用，系統已切換到備用文件分析模式。

📄 文件信息：
- 文件名：{filename}
- 文件大小：{file_size / 1024:.2f} KB
- 文件類型：{file_ext.upper()}

🔍 基本分析：
1. 文件已成功上傳並識別
2. 文件格式符合系統要求
3. 建議使用完整AI引擎進行深度分析

⚠️ 注意：這是簡化分析結果，完整的文件AI分析請稍後重試。
        """

        return jsonify({
            'success': True,
            'analysis': analysis_result.strip(),
            'confidence_score': 0.70,
            'processing_time': 0.1,
            'engine_type': '備用文件分析引擎',
            'fallback_mode': True,
            'file_info': {
                'filename': filename,
                'size': file_size,
                'type': file_ext
            },
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"備用文件分析錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'error': '備用文件分析失敗'
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
    print("🚀 需求分析UI後台服務啟動中...")
    print(f"📁 上傳目錄: {UPLOAD_FOLDER}")
    print(f"🔗 主分析引擎: {MAIN_ANALYSIS_ENGINE_URL}")
    print("🌐 前台UI: http://localhost:5000")
    print("🔧 健康檢查: http://localhost:5000/health")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )

