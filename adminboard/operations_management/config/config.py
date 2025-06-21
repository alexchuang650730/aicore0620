"""
運營管理中心配置文件
Operations Management Center Configuration
"""

# 服務配置
SERVICE_CONFIG = {
    'host': '0.0.0.0',
    'port': 5001,
    'debug': False
}

# 監控配置
MONITORING_CONFIG = {
    'check_interval': 30,  # 檢查間隔(秒)
    'alert_thresholds': {
        'cpu': 80.0,      # CPU使用率告警閾值(%)
        'memory': 90.0,   # 記憶體使用率告警閾值(%)
        'disk': 85.0      # 磁碟使用率告警閾值(%)
    },
    'request_timeout': 5   # 服務檢查超時時間(秒)
}

# 數據庫配置
DATABASE_CONFIG = {
    'file': 'operations_management.db',
    'backup_interval': 3600  # 備份間隔(秒)
}

# 監控的服務列表 (修正測試組件服務配置)
MONITORED_SERVICES = {
    "需求分析服務": {
        "url": "http://localhost:5000/health",
        "port": 5000,
        "description": "需求分析UI後端服務",
        "critical": True
    },
    "發布管理服務": {
        "url": "http://localhost:5002/health", 
        "port": 5002,
        "description": "發布管理UI後端服務",
        "critical": False
    },
    "測試管理工作流MCP": {
        "url": "http://localhost:8321/health",
        "port": 8321,
        "description": "純AI驅動測試管理工作流MCP服務",
        "critical": True
    },
    "AI分析引擎": {
        "url": "http://localhost:8888/health",
        "port": 8888,
        "description": "純AI驅動需求分析引擎",
        "critical": True
    },
    "運營工作流MCP": {
        "url": "http://localhost:8091/health",
        "port": 8091,
        "description": "純AI驅動運營工作流MCP服務",
        "critical": True
    },
    "運營分析引擎": {
        "url": "http://localhost:8100/health",
        "port": 8100,
        "description": "純AI驅動運營分析引擎",
        "critical": True
    }
}

# 告警配置
ALERT_CONFIG = {
    'max_alerts': 100,     # 最大告警數量
    'auto_resolve_hours': 24,  # 自動解決告警時間(小時)
    'severity_levels': ['info', 'warning', 'critical']
}

# 日誌配置
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'operations_management.log',
    'max_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

