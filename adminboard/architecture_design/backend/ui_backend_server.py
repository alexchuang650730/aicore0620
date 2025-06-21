# -*- coding: utf-8 -*-
"""
架構設計UI相關後台API服務
Architecture Design UI Backend API Service
專門為架構設計前台UI提供API支持的後台服務
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

# 導入配置
try:
    from config.config import *
except ImportError:
    # 默認配置
    UI_BACKEND_HOST = "0.0.0.0"
    UI_BACKEND_PORT = 5002
    ARCHITECTURE_DESIGN_MCP_URL = "http://localhost:8306"
    UPLOAD_FOLDER = "uploads"
    ALLOWED_EXTENSIONS = ['txt', 'pdf', 'doc', 'docx', 'md', 'json', 'yaml']
    MAX_FILE_SIZE = 16 * 1024 * 1024
    FALLBACK_MODE_ENABLED = True

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 配置
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# 確保上傳目錄存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """檢查文件類型是否允許"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class ArchitectureDesignUIServer:
    """架構設計UI後台服務器"""
    
    def __init__(self):
        self.service_name = "architecture_design_ui_server"
        self.version = "1.0.0"
        self.main_engine_url = ARCHITECTURE_DESIGN_MCP_URL
        
    async def analyze_architecture_requirement(self, requirement, context=None):
        """分析架構設計需求"""
        try:
            # 嘗試調用主架構設計引擎
            payload = {
                'requirement': requirement,
                'context': context,
                'timestamp': datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.main_engine_url}/api/analyze",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"主引擎響應異常: {response.status_code}")
                return self._fallback_analysis(requirement)
                
        except Exception as e:
            logger.error(f"調用主引擎失敗: {str(e)}")
            return self._fallback_analysis(requirement)
    
    def _fallback_analysis(self, requirement):
        """降級模式分析"""
        if not FALLBACK_MODE_ENABLED:
            return {"error": "服務暫時不可用"}
            
        return {
            "analysis_type": "fallback_mode",
            "requirement": requirement,
            "basic_analysis": f"基於需求 '{requirement}' 的基礎架構分析",
            "recommendations": [
                "建議進行詳細的需求分析",
                "考慮系統的可擴展性和維護性", 
                "評估技術選型的適用性",
                "制定分階段實施計劃"
            ],
            "note": "當前為降級模式，建議檢查系統組件狀態"
        }
    
    def get_system_status(self):
        """獲取系統狀態"""
        try:
            # 檢查主引擎狀態
            response = requests.get(f"{self.main_engine_url}/health", timeout=10)
            main_engine_status = "healthy" if response.status_code == 200 else "unhealthy"
        except:
            main_engine_status = "unhealthy"
            
        return {
            "overall_status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "ui_server": {
                "status": "healthy",
                "version": self.version,
                "uptime": "running"
            },
            "main_engine": {
                "status": main_engine_status,
                "url": self.main_engine_url,
                "description": "架構設計MCP主引擎"
            },
            "fallback_available": FALLBACK_MODE_ENABLED
        }

# 創建服務實例
ui_server = ArchitectureDesignUIServer()

@app.route('/')
def index():
    """返回前端頁面"""
    try:
        return send_from_directory('../frontend', 'index.html')
    except Exception as e:
        logger.error(f"無法加載前端頁面: {str(e)}")
        return jsonify({"error": "前端頁面加載失敗"}), 500

@app.route('/health')
def health_check():
    """健康檢查端點"""
    return jsonify({
        "status": "healthy",
        "service": "Architecture Design UI Backend",
        "version": ui_server.version,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/status')
def api_status():
    """API狀態檢查"""
    return jsonify(ui_server.get_system_status())

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """架構設計分析API"""
    try:
        data = request.get_json()
        if not data or 'requirement' not in data:
            return jsonify({"error": "缺少必需的 'requirement' 參數"}), 400
            
        requirement = data['requirement']
        context = data.get('context', '')
        
        # 使用asyncio運行異步分析
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            ui_server.analyze_architecture_requirement(requirement, context)
        )
        loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"分析請求處理失敗: {str(e)}")
        return jsonify({"error": "分析請求處理失敗"}), 500

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """文件上傳API"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "沒有文件被上傳"}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "沒有選擇文件"}), 400
            
        if file and allowed_file(file.filename):
            filename = f"{int(time.time())}_{file.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            return jsonify({
                "success": True,
                "message": f"文件 {file.filename} 上傳成功",
                "filename": filename,
                "size": os.path.getsize(filepath)
            })
        else:
            return jsonify({"error": "不支持的文件類型"}), 400
            
    except Exception as e:
        logger.error(f"文件上傳失敗: {str(e)}")
        return jsonify({"error": "文件上傳失敗"}), 500

@app.route('/api/architecture/templates')
def api_architecture_templates():
    """獲取架構設計模板"""
    try:
        templates = getattr(globals(), 'ARCHITECTURE_TEMPLATES', {
            'web_application': '標準Web應用架構',
            'mobile_backend': '移動應用後端架構',
            'data_platform': '數據平台架構'
        })
        return jsonify(templates)
    except Exception as e:
        logger.error(f"獲取模板失敗: {str(e)}")
        return jsonify({"error": "獲取模板失敗"}), 500

@app.route('/api/architecture/types')
def api_architecture_types():
    """獲取支持的架構類型"""
    try:
        types = getattr(globals(), 'SUPPORTED_ARCHITECTURE_TYPES', [
            'microservices_architecture',
            'monolithic_architecture',
            'serverless_architecture'
        ])
        return jsonify(types)
    except Exception as e:
        logger.error(f"獲取架構類型失敗: {str(e)}")
        return jsonify({"error": "獲取架構類型失敗"}), 500

@app.errorhandler(404)
def not_found(error):
    """404錯誤處理"""
    return jsonify({"error": "API端點不存在"}), 404

@app.errorhandler(500)
def internal_error(error):
    """500錯誤處理"""
    return jsonify({"error": "內部服務器錯誤"}), 500

if __name__ == '__main__':
    logger.info(f"啟動架構設計UI後台服務器...")
    logger.info(f"主引擎URL: {ARCHITECTURE_DESIGN_MCP_URL}")
    logger.info(f"服務地址: http://{UI_BACKEND_HOST}:{UI_BACKEND_PORT}")
    
    app.run(
        host=UI_BACKEND_HOST,
        port=UI_BACKEND_PORT,
        debug=False
    )

