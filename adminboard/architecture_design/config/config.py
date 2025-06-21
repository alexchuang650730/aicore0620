# 架構設計UI系統配置文件

# 服務配置
UI_BACKEND_HOST = "0.0.0.0"
UI_BACKEND_PORT = 5002
DEBUG_MODE = False

# 架構設計MCP引擎配置
ARCHITECTURE_DESIGN_MCP_URL = "http://localhost:8306"
ARCHITECTURE_ANALYSIS_ENGINE_URL = "http://localhost:8306"
ARCHITECTURE_ENGINE_TIMEOUT = 60

# 文件上傳配置
UPLOAD_FOLDER = "uploads"
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'html', 'htm', 'md', 'csv', 'json', 'yaml', 'yml', 'xml', 'drawio']

# 日誌配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 安全配置
SECRET_KEY = "architecture-design-secret-key"
CORS_ORIGINS = ["*"]  # 生產環境中應該限制具體域名

# 備用分析配置
FALLBACK_MODE_ENABLED = True
FALLBACK_CONFIDENCE_SCORE = 0.75

# 架構設計特定配置
SUPPORTED_ARCHITECTURE_TYPES = [
    'microservices_architecture',
    'monolithic_architecture', 
    'serverless_architecture',
    'event_driven_architecture',
    'layered_architecture',
    'hexagonal_architecture',
    'clean_architecture',
    'distributed_architecture'
]

# 架構分析組件配置
ARCHITECTURE_ANALYSIS_COMPONENTS = [
    'architecture_orchestrator',
    'architecture_design_mcp',
    'architecture_design_ai_engine',
    'pure_ai_architecture_design_system'
]

# 架構設計模板配置
ARCHITECTURE_TEMPLATES = {
    'web_application': '標準Web應用架構',
    'mobile_backend': '移動應用後端架構',
    'data_platform': '數據平台架構',
    'iot_system': 'IoT系統架構',
    'ai_ml_platform': 'AI/ML平台架構',
    'enterprise_integration': '企業整合架構'
}

# 導出格式配置
EXPORT_FORMATS = ['json', 'yaml', 'markdown', 'pdf', 'drawio']

# 可視化配置
VISUALIZATION_ENABLED = True
DIAGRAM_FORMATS = ['svg', 'png', 'pdf']

