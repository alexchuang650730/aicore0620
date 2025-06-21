# 運營工作流UI系統配置文件

# 服務配置
UI_BACKEND_HOST = "0.0.0.0"
UI_BACKEND_PORT = 5001
DEBUG_MODE = False

# 運營工作流引擎配置
OPERATIONS_WORKFLOW_MCP_URL = "http://localhost:8091"
OPERATIONS_ANALYSIS_ENGINE_URL = "http://localhost:8100"
OPERATIONS_ENGINE_TIMEOUT = 60

# 文件上傳配置
UPLOAD_FOLDER = "uploads"
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'html', 'htm', 'md', 'csv', 'json', 'yaml', 'yml', 'log']

# 日誌配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 安全配置
SECRET_KEY = "operations-workflow-secret-key"
CORS_ORIGINS = ["*"]  # 生產環境中應該限制具體域名

# 備用分析配置
FALLBACK_MODE_ENABLED = True
FALLBACK_CONFIDENCE_SCORE = 0.75

# 運營工作流特定配置
SUPPORTED_OPERATIONS_TYPES = [
    'release_operations',
    'monitoring_operations', 
    'security_operations',
    'infrastructure_operations',
    'incident_operations',
    'automation_operations',
    'general_operations'
]

# Release Manager 整合配置
RELEASE_MANAGER_INTEGRATION = True
SUPPORTED_COMPONENTS = [
    'deployment_analysis_mcp',
    'monitoring_analysis_mcp',
    'performance_analysis_mcp',
    'security_operations_mcp',
    'infrastructure_operations_mcp',
    'operations_analysis_mcp'
]

