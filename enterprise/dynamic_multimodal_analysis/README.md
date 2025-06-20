# 多模態需求分析系統架構

## 系統概述

這是一個整合了MCP組件和產品編排系統的多模態需求分析系統，具備主動提問、多輪對話和文檔處理能力。

## 核心組件

### 1. 主要服務
- `multimodal_requirement_analysis_service.py` - 多模態需求分析HTTP服務（主入口）
- `interactive_requirement_analysis_workflow_mcp.py` - 互動式需求分析工作流MCP

### 2. 文檔處理
- `multimodal_document_processor.py` - 多模態文檔處理器
- 支持格式：txt, pdf, doc, docx, png, jpg, jpeg, gif, bmp, tiff, webp, csv, xls, xlsx, md, py, js, html, css, json, xml

### 3. AI增強組件
- `ai_requirement_analysis_mcp.py` - AI增強需求分析MCP
- `sequential_thinking_adapter.py` - 序列思考適配器
- `smart_tool_engine.py` - 智能工具引擎
- `incremental_engine.py` - 增量分析引擎

### 4. 測試文件
- `test_multimodal_service.py` - 多模態服務測試腳本
- `test_ai_requirement_analysis.py` - AI需求分析測試
- `test_requirement_analysis_api.py` - API測試腳本

## 部署說明

### 1. 安裝依賴
```bash
pip3 install flask flask-cors pillow pymupdf python-docx pandas openpyxl anthropic
```

### 2. 啟動服務
```bash
python3 multimodal_requirement_analysis_service.py
```

### 3. 服務地址
- 本地地址：http://localhost:8300
- 健康檢查：http://localhost:8300/health
- API文檔：http://localhost:8300/api/info

## API接口

### 主要端點
- `POST /api/start-session` - 開始需求分析會話
- `POST /api/analyze-text` - 分析文本需求
- `POST /api/upload-document` - 上傳文檔分析
- `POST /api/answer-question` - 回答系統問題
- `GET /api/get-session` - 獲取會話狀態
- `GET /api/sessions` - 列出活躍會話

## 系統特色

### 1. 互動式分析
- 主動識別需求缺口
- 智能生成澄清問題
- 多輪對話式完善
- 動態調整問題策略

### 2. 多模態處理
- 支持22種文件格式
- OCR文字識別
- 文檔結構分析
- 內容智能提取

### 3. AI增強能力
- 大語言模型整合
- 結構化思考推理
- 智能工具調用
- 增量分析比較

## 使用示例

### 1. 開始分析會話
```bash
curl -X POST http://localhost:8300/api/start-session \
  -H "Content-Type: application/json" \
  -d '{"requirement": "開發一個電商網站"}'
```

### 2. 上傳文檔分析
```bash
curl -X POST http://localhost:8300/api/upload-document \
  -F "file=@document.pdf" \
  -F "session_id="
```

## 技術架構

### 1. 架構層次
- **HTTP服務層** - Flask Web服務
- **工作流層** - 互動式需求分析工作流
- **適配器層** - 各種功能適配器
- **處理器層** - 文檔和數據處理

### 2. 組件關係
```
HTTP服務 → 工作流MCP → 適配器組件 → 處理器
    ↓           ↓           ↓         ↓
  API接口   主動提問   AI增強    文檔處理
```

## 注意事項

1. **API密鑰配置**：需要配置OpenAI或Anthropic API密鑰以啟用AI功能
2. **文件處理**：大文件處理可能需要較長時間
3. **會話管理**：系統會維護活躍會話，建議定期清理
4. **安全考慮**：生產環境請配置適當的安全措施

## 開發說明

這個系統展示了：
- MCP組件架構的實際應用
- 多模態文檔處理能力
- AI增強的需求分析流程
- 互動式用戶體驗設計

雖然某些組件還處於基礎階段，但提供了完整的架構框架，可以根據實際需求進一步完善和擴展。

## 版本信息

- 版本：1.0.0
- 創建日期：2025-06-18
- 開發者：Manus AI
- 許可證：MIT

