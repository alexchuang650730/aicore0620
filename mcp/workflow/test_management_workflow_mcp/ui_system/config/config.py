# 測試組件管理UI系統配置文件

# 服務配置
UI_BACKEND_HOST = "0.0.0.0"
UI_BACKEND_PORT = 5001
DEBUG_MODE = False

# 主分析引擎配置
CODING_WORKFLOW_URL = "http://localhost:8888"
TEST_WORKFLOW_URL = "http://localhost:8321"
ENGINE_TIMEOUT = 60

# 日誌配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 安全配置
SECRET_KEY = "test-component-management-secret-key"
CORS_ORIGINS = ["*"]  # 生產環境中應該限制具體域名

# 架構配置
ARCHITECTURE_VERSION = "3.0.0"
CODING_WORKFLOW_COMPONENTS = 6  # 1個生成器 + 5個分析器
TEST_WORKFLOW_COMPONENTS = 4    # 4個測試組件

# 組件端口配置
COMPONENT_PORTS = {
    # Coding Workflow Components
    "kilocode_mcp": 8317,
    "code_quality_mcp": 8310,
    "architecture_design_mcp": 8311,
    "performance_analysis_mcp": 8312,  # 保留在Coding Workflow
    "security_audit_mcp": 8313,
    "code_documentation_mcp": 8315,
    "dependency_analysis_mcp": 8316,
    
    # Test Management Workflow Components
    "testing_strategy_mcp": 8314,      # 移動到Test Management Workflow
    "test_execution_mcp": 8318,
    "test_automation_mcp": 8319,
    "quality_assurance_mcp": 8320
}

# 重構驗證配置
ARCHITECTURE_VALIDATION = {
    "performance_analysis_location": "coding_workflow",
    "testing_strategy_location": "test_management_workflow",
    "expected_coding_components": 6,
    "expected_test_components": 4
}

