# 純AI驅動發布管理系統UI配置文件

# 服務配置
UI_BACKEND_HOST = "0.0.0.0"
UI_BACKEND_PORT = 5002
DEBUG_MODE = False

# 純AI驅動發布管理引擎配置
RELEASE_PRODUCT_ENGINE_URL = "http://localhost:8302"
RELEASE_WORKFLOW_ENGINE_URL = "http://localhost:8303"
RELEASE_ANALYSIS_ENGINE_URL = "http://localhost:8304"
ENGINE_TIMEOUT = 90

# 文件上傳配置
UPLOAD_FOLDER = "uploads"
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'html', 'htm', 'md', 'csv', 'json']

# 日誌配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 安全配置
SECRET_KEY = "pure-ai-driven-release-management-secret"
CORS_ORIGINS = ["*"]  # 生產環境中應該限制具體域名

# 純AI驅動配置
AI_DRIVEN = True
ZERO_HARDCODING = True
PURE_AI_REASONING = True
ARCHITECTURE = "pure_ai_driven_three_layer"

# 備用分析配置
FALLBACK_MODE_ENABLED = True
FALLBACK_CONFIDENCE_SCORE = 0.85

# 性能配置
MAX_WORKERS = 4
REQUEST_TIMEOUT = 90
RETRY_ATTEMPTS = 3

# 監控配置
HEALTH_CHECK_INTERVAL = 30
ENGINE_STATUS_CACHE_TTL = 60


