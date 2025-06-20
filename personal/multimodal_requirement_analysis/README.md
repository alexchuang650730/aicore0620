# 多模態需求分析系統

## 概述

多模態需求分析系統是PowerAutomation平台的企業級組件，提供智能化的需求分析和文檔處理能力。

## 功能特色

### 🤖 多模型支持
- **MiniMax M1-80k**: 高性能中文模型，成本低廉，速度快
- **Gemini Flash**: Google最新模型，速度極快，適合快速分析
- **Gemini Pro**: Google專業模型，分析深度更好，適合複雜需求
- **Claude Sonnet**: Anthropic精準模型，邏輯推理能力強
- **智能選擇**: 系統根據任務類型自動選擇最適合的模型

### 📄 多模態文檔處理
- 支援22種文件格式：PDF, DOC, DOCX, TXT, MD, PNG, JPG, CSV, XLS等
- 智能文檔內容提取和分析
- OCR文字識別和結構化處理

### 🔄 三種分析模式
1. **文本需求分析** - 純文字描述分析
2. **文檔內容分析** - 純文檔分析
3. **文本+文檔綜合分析** - 結合文字和文檔

### 💬 互動式分析
- AI主動提問和澄清
- 多輪對話支持
- 結構化需求輸出

## 技術架構

### 核心組件
- `multimodal_service.py` - 主HTTP服務
- `interactive_requirement_analysis_workflow_mcp.py` - 互動式工作流MCP
- `multimodal_document_processor.py` - 多模態文檔處理器

### MCP組件整合
- Cloud Search MCP - 雲端視覺搜索
- Sequential Thinking Adapter - 序列思考適配器
- Smart Tool Engine - 智能工具引擎
- Incremental Engine - 增量分析引擎

## 部署說明

### 環境要求
```bash
pip3 install flask flask-cors pillow pymupdf python-docx pandas openpyxl huggingface_hub
```

### 啟動服務
```bash
cd src/
python3 multimodal_service.py
```

### 配置說明
- 設置HuggingFace Token用於MiniMax模型
- 配置其他AI模型的API密鑰
- 調整模型選擇策略

## API接口

### 主要端點
- `GET /` - 互動式Web界面
- `GET /health` - 健康檢查
- `POST /api/analyze` - 需求分析
- `POST /api/upload-document` - 文檔上傳分析

### 使用示例
```bash
# 需求分析
curl -X POST http://localhost:8300/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"requirement": "我想開發一個電商網站", "model": "minimax"}'

# 文檔上傳
curl -X POST http://localhost:8300/api/upload-document \
  -F "file=@document.pdf" \
  -F "model=minimax"
```

## 版本歷史

### v1.1 (2025-06-19)
- ✅ 添加MiniMax模型支持
- ✅ 實現模型選擇功能
- ✅ 優化繁體中文支持
- ✅ 增強文檔上傳功能
- ✅ 改進響應式UI設計

### v1.0 (2025-06-19)
- ✅ 基礎多模態需求分析功能
- ✅ 互動式工作流MCP
- ✅ 文檔處理能力
- ✅ Web界面

