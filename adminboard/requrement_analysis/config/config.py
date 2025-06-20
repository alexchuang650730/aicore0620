# 需求分析UI系統配置文件

# 服務配置
UI_BACKEND_HOST = "0.0.0.0"
UI_BACKEND_PORT = 5000
DEBUG_MODE = False

# 主分析引擎配置
MAIN_ANALYSIS_ENGINE_URL = "http://localhost:8888"
MAIN_ENGINE_TIMEOUT = 60

# 文件上傳配置
UPLOAD_FOLDER = "uploads"
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'html', 'htm', 'md', 'csv']

# 日誌配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 安全配置
SECRET_KEY = "your-secret-key-here"
CORS_ORIGINS = ["*"]  # 生產環境中應該限制具體域名

# 備用分析配置
FALLBACK_MODE_ENABLED = True
FALLBACK_CONFIDENCE_SCORE = 0.75

