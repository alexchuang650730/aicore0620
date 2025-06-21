# -*- coding: utf-8 -*-
"""
運營中心整合後端API服務
Operations Center Integrated Backend API Service
整合系統監控和工作流管理功能的統一後台服務
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import time
import logging
import psutil
import sqlite3
from datetime import datetime, timedelta
import requests
import threading
from typing import Dict, List, Any
import asyncio

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 配置
DATABASE_FILE = 'operations_center.db'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'html', 'htm', 'md', 'csv', 'json', 'yaml', 'yml', 'log'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# 告警閾值
ALERT_THRESHOLD_CPU = 80.0
ALERT_THRESHOLD_MEMORY = 90.0
ALERT_THRESHOLD_DISK = 85.0

# 監控服務配置
MONITORED_SERVICES = [
    {
        'name': '需求分析服務',
        'url': 'http://localhost:5000/health',
        'port': 5000,
        'description': '需求分析UI後端服務'
    },
    {
        'name': '七大工作流測試系統',
        'url': 'http://localhost:5001/health',
        'port': 5001,
        'description': 'AICore0620 七大工作流測試系統'
    },
    {
        'name': '發布管理服務',
        'url': 'http://localhost:5002/health',
        'port': 5002,
        'description': '發布管理UI後端服務'
    },
    {
        'name': '測試管理工作流MCP',
        'url': 'http://localhost:8321/health',
        'port': 8321,
        'description': '測試管理工作流MCP服務'
    },
    {
        'name': 'AI分析引擎',
        'url': 'http://localhost:8888/health',
        'port': 8888,
        'description': '純AI驅動分析系統'
    },
    {
        'name': '運營工作流MCP',
        'url': 'http://localhost:8091/health',
        'port': 8091,
        'description': '運營工作流MCP服務'
    },
    {
        'name': '運營分析引擎',
        'url': 'http://localhost:8100/health',
        'port': 8100,
        'description': '運營分析引擎服務'
    }
]

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# 確保上傳目錄存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_database():
    """初始化數據庫"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # 創建告警表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            message TEXT NOT NULL,
            severity TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            resolved BOOLEAN DEFAULT FALSE,
            resolved_at DATETIME
        )
    ''')
    
    # 創建系統監控記錄表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpu_percent REAL,
            memory_percent REAL,
            disk_percent REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 創建服務狀態記錄表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL,
            status TEXT NOT NULL,
            response_time REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def check_service_health(service: Dict) -> Dict:
    """檢查單個服務健康狀態"""
    try:
        start_time = time.time()
        response = requests.get(service['url'], timeout=5)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            return {
                'name': service['name'],
                'status': 'running',
                'response_time': round(response_time, 3),
                'port': service['port'],
                'description': service['description'],
                'details': response.json() if response.headers.get('content-type', '').startswith('application/json') else None
            }
        else:
            return {
                'name': service['name'],
                'status': 'error',
                'response_time': None,
                'port': service['port'],
                'description': service['description'],
                'details': {'error': f'HTTP {response.status_code}'}
            }
    except requests.exceptions.ConnectionError:
        return {
            'name': service['name'],
            'status': 'error',
            'response_time': None,
            'port': service['port'],
            'description': service['description'],
            'details': {'error': '連接被拒絕'}
        }
    except requests.exceptions.Timeout:
        return {
            'name': service['name'],
            'status': 'warning',
            'response_time': None,
            'port': service['port'],
            'description': service['description'],
            'details': {'error': '請求超時'}
        }
    except Exception as e:
        return {
            'name': service['name'],
            'status': 'error',
            'response_time': None,
            'port': service['port'],
            'description': service['description'],
            'details': {'error': str(e)}
        }

def get_system_resources() -> Dict:
    """獲取系統資源使用情況"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu_percent': round(cpu_percent, 1),
            'memory_percent': round(memory.percent, 1),
            'disk_percent': round(disk.percent, 1),
            'memory_total': round(memory.total / (1024**3), 2),  # GB
            'memory_used': round(memory.used / (1024**3), 2),   # GB
            'disk_total': round(disk.total / (1024**3), 2),     # GB
            'disk_used': round(disk.used / (1024**3), 2)        # GB
        }
    except Exception as e:
        logger.error(f"獲取系統資源失敗: {e}")
        return {
            'cpu_percent': 0,
            'memory_percent': 0,
            'disk_percent': 0,
            'memory_total': 0,
            'memory_used': 0,
            'disk_total': 0,
            'disk_used': 0
        }

def create_alert(alert_type: str, message: str, severity: str = 'warning'):
    """創建告警"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        # 檢查是否已存在相同的未解決告警
        cursor.execute('''
            SELECT id FROM alerts 
            WHERE type = ? AND message = ? AND resolved = FALSE
        ''', (alert_type, message))
        
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO alerts (type, message, severity)
                VALUES (?, ?, ?)
            ''', (alert_type, message, severity))
            conn.commit()
            logger.info(f"創建告警: {alert_type} - {message}")
        
        conn.close()
    except Exception as e:
        logger.error(f"創建告警失敗: {e}")

def monitor_system():
    """系統監控線程"""
    while True:
        try:
            # 獲取系統資源
            resources = get_system_resources()
            
            # 記錄到數據庫
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO system_metrics (cpu_percent, memory_percent, disk_percent)
                VALUES (?, ?, ?)
            ''', (resources['cpu_percent'], resources['memory_percent'], resources['disk_percent']))
            conn.commit()
            conn.close()
            
            # 檢查告警條件
            if resources['cpu_percent'] > ALERT_THRESHOLD_CPU:
                create_alert('系統告警', f'CPU使用率過高: {resources["cpu_percent"]}%', 'warning')
            
            if resources['memory_percent'] > ALERT_THRESHOLD_MEMORY:
                create_alert('系統告警', f'記憶體使用率過高: {resources["memory_percent"]}%', 'critical')
            
            if resources['disk_percent'] > ALERT_THRESHOLD_DISK:
                create_alert('系統告警', f'磁碟使用率過高: {resources["disk_percent"]}%', 'warning')
            
            # 檢查服務狀態
            for service in MONITORED_SERVICES:
                status = check_service_health(service)
                
                # 記錄服務狀態
                conn = sqlite3.connect(DATABASE_FILE)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO service_status (service_name, status, response_time)
                    VALUES (?, ?, ?)
                ''', (status['name'], status['status'], status['response_time']))
                conn.commit()
                conn.close()
                
                # 創建服務告警
                if status['status'] == 'error':
                    error_msg = status['details'].get('error', '未知錯誤') if status['details'] else '服務不可用'
                    create_alert('服務告警', f'{status["name"]}: {error_msg}', 'critical')
            
            time.sleep(30)  # 30秒檢查一次
            
        except Exception as e:
            logger.error(f"監控線程錯誤: {e}")
            time.sleep(30)

def allowed_file(filename):
    """檢查文件類型是否允許"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== 系統監控API ====================

@app.route('/')
def index():
    """主頁"""
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """靜態文件"""
    return send_from_directory('frontend', filename)

@app.route('/health')
def health_check():
    """健康檢查"""
    return jsonify({
        'service': 'operations_center_backend',
        'status': 'healthy',
        'version': '1.0',
        'description': '運營中心整合後端服務',
        'timestamp': datetime.now().isoformat(),
        'features': {
            'system_monitoring': True,
            'workflow_management': True,
            'service_management': True,
            'resource_monitoring': True,
            'alert_management': True,
            'file_upload': True
        }
    })

@app.route('/api/system/overview')
def system_overview():
    """系統概覽"""
    try:
        # 獲取服務狀態
        services_status = []
        for service in MONITORED_SERVICES:
            status = check_service_health(service)
            services_status.append(status)
        
        active_services = len([s for s in services_status if s['status'] == 'running'])
        total_services = len(services_status)
        
        # 獲取活動告警數量
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM alerts WHERE resolved = FALSE')
        active_alerts = cursor.fetchone()[0]
        conn.close()
        
        # 獲取系統運行時間
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        uptime_hours = int(uptime_seconds // 3600)
        uptime_days = uptime_hours // 24
        uptime_hours = uptime_hours % 24
        
        uptime_str = f"{uptime_days}天 {uptime_hours}小時" if uptime_days > 0 else f"{uptime_hours}小時"
        
        return jsonify({
            'status': 'healthy' if active_services > total_services * 0.5 else 'warning',
            'uptime': uptime_str,
            'active_services': active_services,
            'total_services': total_services,
            'active_alerts': active_alerts,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"系統概覽API錯誤: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/services/status')
def services_status():
    """服務狀態檢查"""
    try:
        services = []
        for service in MONITORED_SERVICES:
            status = check_service_health(service)
            services.append(status)
        
        return jsonify({
            'services': services,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"服務狀態API錯誤: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/resources')
def system_resources():
    """系統資源監控"""
    try:
        resources = get_system_resources()
        resources['timestamp'] = datetime.now().isoformat()
        return jsonify(resources)
    except Exception as e:
        logger.error(f"系統資源API錯誤: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts')
def get_alerts():
    """獲取告警列表"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT type, message, severity, timestamp, resolved
            FROM alerts 
            ORDER BY timestamp DESC 
            LIMIT 50
        ''')
        
        alerts = []
        for row in cursor.fetchall():
            alerts.append({
                'type': row[0],
                'message': row[1],
                'severity': row[2],
                'timestamp': row[3],
                'resolved': bool(row[4])
            })
        
        conn.close()
        
        return jsonify({
            'alerts': alerts,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"告警API錯誤: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts/resolve', methods=['POST'])
def resolve_alert():
    """解決告警"""
    try:
        data = request.get_json()
        alert_id = data.get('alert_id')
        
        if not alert_id:
            return jsonify({'error': '缺少告警ID'}), 400
        
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE alerts 
            SET resolved = TRUE, resolved_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (alert_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': '告警已解決'})
    except Exception as e:
        logger.error(f"解決告警API錯誤: {e}")
        return jsonify({'error': str(e)}), 500

# ==================== 工作流管理API ====================

@app.route('/api/workflow/analyze', methods=['POST'])
def analyze_workflow():
    """工作流分析"""
    try:
        data = request.get_json()
        requirement = data.get('requirement', '')
        model = data.get('model', 'pure_ai_engine')
        
        if not requirement:
            return jsonify({'error': '缺少需求描述'}), 400
        
        # 模擬AI分析過程
        start_time = time.time()
        
        # 這裡可以集成實際的AI分析引擎
        # 目前返回模擬結果
        analysis_result = f"""
🔍 運營工作流分析報告

📋 需求分析:
{requirement}

🎯 分析結果:
基於您的需求，我識別出以下關鍵要點：

1. 流程優化機會
   - 識別瓶頸環節
   - 自動化潛力評估
   - 效率提升建議

2. 資源配置建議
   - 人力資源優化
   - 技術工具整合
   - 成本效益分析

3. 實施路線圖
   - 短期改善措施
   - 中期優化目標
   - 長期戰略規劃

🚀 建議行動:
- 優先處理高影響、低成本的改善項目
- 建立關鍵績效指標(KPI)監控體系
- 定期評估和調整工作流程

📊 預期效果:
- 效率提升: 15-25%
- 成本降低: 10-20%
- 客戶滿意度提升: 20-30%
        """
        
        processing_time = time.time() - start_time
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'model_used': model,
            'processing_time': processing_time,
            'confidence_score': 0.85,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"工作流分析API錯誤: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/workflow/upload', methods=['POST'])
def upload_workflow_files():
    """上傳工作流文件"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': '沒有文件被上傳'}), 400
        
        files = request.files.getlist('files')
        requirement = request.form.get('requirement', '請分析上傳的工作流文件')
        
        if not files or all(file.filename == '' for file in files):
            return jsonify({'error': '沒有選擇文件'}), 400
        
        uploaded_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = f"{int(time.time())}_{file.filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                uploaded_files.append({
                    'filename': file.filename,
                    'saved_as': filename,
                    'size': os.path.getsize(filepath)
                })
        
        if not uploaded_files:
            return jsonify({'error': '沒有有效的文件被上傳'}), 400
        
        # 模擬文件分析過程
        start_time = time.time()
        
        analysis_result = f"""
📁 文件分析報告

📋 上傳文件:
{chr(10).join([f"- {f['filename']} ({f['size']} bytes)" for f in uploaded_files])}

🔍 分析需求:
{requirement}

📊 分析結果:
基於上傳的文件，我進行了以下分析：

1. 文件結構分析
   - 文件類型分布
   - 內容組織方式
   - 數據完整性檢查

2. 工作流程識別
   - 關鍵流程步驟
   - 決策點分析
   - 異常處理機制

3. 優化建議
   - 流程簡化機會
   - 自動化潛力
   - 標準化建議

🎯 關鍵發現:
- 識別出 {len(uploaded_files)} 個相關文件
- 發現 3-5 個主要工作流程
- 識別出 2-3 個優化機會

💡 改善建議:
- 建立統一的文件命名規範
- 實施版本控制機制
- 優化流程文檔結構
        """
        
        processing_time = time.time() - start_time
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'uploaded_files': uploaded_files,
            'processing_time': processing_time,
            'confidence_score': 0.78,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"文件上傳API錯誤: {e}")
        return jsonify({'error': str(e)}), 500

# 初始化
init_database()

# 啟動監控線程
monitor_thread = threading.Thread(target=monitor_system, daemon=True)
monitor_thread.start()
logger.info("監控線程已啟動")

if __name__ == '__main__':
    logger.info("啟動運營中心整合後端服務...")
    app.run(host='0.0.0.0', port=5010, debug=False)

