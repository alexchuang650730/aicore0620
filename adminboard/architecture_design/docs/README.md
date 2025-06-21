# Architecture Design Admin UI System

## 📋 系統概述

純AI驅動架構設計系統的Web管理界面，提供直觀易用的架構設計分析和管理功能。

## 🎯 功能特性

### 核心功能
- **智能架構分析**: 基於AI的架構設計需求分析
- **多種架構類型**: 支持微服務、單體、無服務器等多種架構
- **可視化設計**: 提供架構圖表和可視化工具
- **模板庫**: 內置常用架構設計模板
- **文件處理**: 支持多種格式的文檔上傳和分析

### 技術特色
- **零硬編碼**: 100%純AI驅動的分析決策
- **三層架構**: Product-Workflow-Adapter清晰分離
- **降級模式**: 主引擎不可用時自動降級
- **實時監控**: 系統狀態實時監控和健康檢查

## 🏗️ 系統架構

### 目錄結構
```
adminboard/architecture_design/
├── backend/                    # 後端API服務
│   ├── __init__.py
│   └── ui_backend_server.py   # Flask API服務器
├── config/                     # 配置管理
│   ├── __init__.py
│   └── config.py              # 系統配置
├── docs/                       # 文檔說明
│   └── README.md              # 本文檔
└── frontend/                   # 前端界面
    └── index.html             # 主頁面
```

### 服務架構
- **UI後端**: Flask API服務 (端口5002)
- **MCP引擎**: 純AI架構設計引擎 (端口8306)
- **前端界面**: 響應式Web界面

## 🚀 安裝部署

### 環境要求
- Python 3.9+
- Flask 2.3+
- 相關依賴包

### 安裝步驟

1. **安裝依賴**
```bash
cd adminboard/architecture_design/backend
pip install -r requirements.txt
```

2. **配置系統**
```bash
# 編輯配置文件
vim config/config.py
```

3. **啟動服務**
```bash
# 啟動UI後端
python backend/ui_backend_server.py

# 確保MCP引擎運行
# (參考mcp/workflow/pure_ai_architecture_design_system)
```

### Docker部署
```bash
# 構建鏡像
docker build -t architecture-design-ui .

# 運行容器
docker run -p 5002:5002 architecture-design-ui
```

## 📖 使用指南

### 基本使用

1. **訪問界面**
   - 打開瀏覽器訪問: http://localhost:5002
   - 或使用配置的服務器地址

2. **架構分析**
   - 在需求輸入框中描述架構需求
   - 點擊"開始分析"按鈕
   - 查看AI生成的架構建議

3. **文件上傳**
   - 點擊"上傳文件"按鈕
   - 選擇支持的文件格式
   - 系統自動分析文件內容

4. **模板使用**
   - 瀏覽內置架構模板
   - 選擇適合的模板作為起點
   - 根據需求進行定制

### 高級功能

1. **架構類型選擇**
   - 微服務架構 (Microservices)
   - 單體架構 (Monolithic)
   - 無服務器架構 (Serverless)
   - 事件驅動架構 (Event-Driven)
   - 分層架構 (Layered)
   - 六邊形架構 (Hexagonal)
   - 清潔架構 (Clean)
   - 分布式架構 (Distributed)

2. **導出功能**
   - JSON格式導出
   - YAML格式導出
   - Markdown文檔
   - PDF報告
   - Draw.io圖表

## 🔧 API文檔

### 基礎端點

#### GET /
返回前端主頁面

#### GET /health
健康檢查端點
```json
{
  "status": "healthy",
  "service": "Architecture Design UI Backend",
  "version": "1.0.0",
  "timestamp": "2025-06-21T..."
}
```

#### GET /api/status
系統狀態檢查
```json
{
  "overall_status": "healthy",
  "ui_server": {...},
  "main_engine": {...},
  "fallback_available": true
}
```

### 核心功能端點

#### POST /api/analyze
架構設計分析
```json
// 請求
{
  "requirement": "設計一個電商平台的微服務架構",
  "context": "需要支持高並發和可擴展性"
}

// 響應
{
  "analysis_type": "ai_analysis",
  "architecture_recommendations": [...],
  "technical_considerations": [...],
  "implementation_plan": [...]
}
```

#### POST /api/upload
文件上傳
```json
// 響應
{
  "success": true,
  "message": "文件上傳成功",
  "filename": "architecture_doc.pdf",
  "size": 1024000
}
```

### 架構特定端點

#### GET /api/architecture/templates
獲取架構模板列表

#### GET /api/architecture/types
獲取支持的架構類型

## ⚙️ 配置說明

### 主要配置項

```python
# 服務配置
UI_BACKEND_HOST = "0.0.0.0"
UI_BACKEND_PORT = 5002

# MCP引擎配置
ARCHITECTURE_DESIGN_MCP_URL = "http://localhost:8306"
ARCHITECTURE_ENGINE_TIMEOUT = 60

# 文件上傳配置
UPLOAD_FOLDER = "uploads"
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'doc', 'docx', ...]

# 架構設計特定配置
SUPPORTED_ARCHITECTURE_TYPES = [...]
ARCHITECTURE_TEMPLATES = {...}
```

### 環境變量
- `ARCHITECTURE_MCP_URL`: MCP服務地址
- `UI_PORT`: UI服務端口
- `DEBUG_MODE`: 調試模式開關

## 🔍 故障排除

### 常見問題

1. **服務無法啟動**
   - 檢查端口是否被占用
   - 確認Python依賴是否安裝完整
   - 查看日誌文件獲取詳細錯誤

2. **MCP連接失敗**
   - 確認MCP服務是否運行
   - 檢查配置中的MCP URL
   - 驗證網絡連接

3. **文件上傳失敗**
   - 檢查文件大小限制
   - 確認文件格式是否支持
   - 驗證上傳目錄權限

### 日誌查看
```bash
# 查看服務日誌
tail -f architecture_ui.log

# 查看系統狀態
curl http://localhost:5002/api/status
```

### 性能優化
- 調整MCP連接超時時間
- 優化文件上傳大小限制
- 配置適當的並發處理

## 🔒 安全配置

### 生產環境建議
- 修改默認密鑰
- 限制CORS來源域名
- 配置HTTPS
- 設置文件上傳限制
- 啟用訪問日誌

### 權限管理
- 文件上傳權限控制
- API訪問頻率限制
- 用戶認證集成

## 📊 監控指標

### 關鍵指標
- API響應時間
- 錯誤率統計
- 文件上傳成功率
- MCP連接狀態
- 系統資源使用

### 告警配置
- 服務不可用告警
- 響應時間過長告警
- 錯誤率過高告警

## 🔄 版本更新

### 當前版本: 1.0.0
- 初始版本發布
- 基礎架構分析功能
- 標準化adminboard結構

### 計劃功能
- 架構圖可視化
- 更多導出格式
- 用戶認證系統
- 協作功能

## 📞 技術支持

### 聯繫方式
- 技術文檔: 本README
- 問題反饋: GitHub Issues
- 系統監控: /api/status端點

### 開發團隊
- 架構設計: AI驅動架構分析
- 後端開發: Flask API服務
- 前端開發: 響應式Web界面

---
**文檔版本**: 1.0.0  
**最後更新**: 2025-06-21  
**維護狀態**: 活躍開發中

