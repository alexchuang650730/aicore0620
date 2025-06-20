# 多模態需求分析系統 - 開發者文檔

## 系統架構

### 整體架構圖
```
┌─────────────────────────────────────────────────────────────┐
│                    Web UI Interface                        │
├─────────────────────────────────────────────────────────────┤
│                  Flask HTTP Service                        │
├─────────────────────────────────────────────────────────────┤
│              Model Selection Router                        │
├─────────────────────────────────────────────────────────────┤
│  MiniMax  │  Gemini   │  Claude   │  Auto Selection       │
│   M1-80k  │ Flash/Pro │  Sonnet   │     Engine            │
├─────────────────────────────────────────────────────────────┤
│           Multimodal Document Processor                    │
├─────────────────────────────────────────────────────────────┤
│              Interactive Workflow MCP                      │
├─────────────────────────────────────────────────────────────┤
│                   MCP Components                           │
│  Cloud Search │ Smart Tool │ Sequential │ Incremental     │
└─────────────────────────────────────────────────────────────┘
```

### 核心組件說明

#### 1. Web UI Interface
- 響應式設計，支援桌面和移動設備
- 模型選擇下拉菜單
- 文件拖拽上傳功能
- 實時分析結果展示

#### 2. Flask HTTP Service
- RESTful API設計
- CORS跨域支持
- 文件上傳處理
- 錯誤處理和日誌記錄

#### 3. Model Selection Router
- 智能模型路由
- 負載平衡
- 故障轉移
- 性能監控

#### 4. AI模型整合
- **MiniMax M1-80k**: 中文優化，成本低廉
- **Gemini Flash/Pro**: Google模型，速度快
- **Claude Sonnet**: 邏輯推理強
- **Auto Selection**: 智能選擇最佳模型

## API設計

### 端點規範

#### GET /health
健康檢查端點
```json
{
  "status": "healthy",
  "service": "多模態需求分析服務",
  "version": "繁體中文版 1.1",
  "deployment": "/optnew3",
  "encoding": "UTF-8 繁體中文支持"
}
```

#### POST /api/analyze
需求分析端點
```json
// 請求
{
  "requirement": "需求描述",
  "model": "minimax|gemini_flash|gemini_pro|claude_sonnet|auto"
}

// 響應
{
  "success": true,
  "requirement": "原始需求",
  "model_used": "使用的模型",
  "response_time": 1500,
  "analysis": {
    "complexity": "中等",
    "estimated_time": "2-4週",
    "key_features": ["功能1", "功能2"],
    "questions": ["問題1", "問題2"]
  },
  "confidence": 0.85,
  "next_steps": ["步驟1", "步驟2"]
}
```

#### POST /api/upload-document
文檔上傳分析端點
```json
// 表單數據
file: 文件對象
model: 模型選擇

// 響應
{
  "success": true,
  "file_info": {
    "filename": "文件名",
    "size": 1024,
    "type": "application/pdf"
  },
  "analysis": {
    "content_summary": "內容摘要",
    "key_points": ["要點1", "要點2"],
    "complexity": "複雜度評估"
  }
}
```

## 開發指南

### 添加新模型

1. **在模型函數中添加新模型**
```python
def analyze_with_new_model(requirement):
    """使用新模型進行分析"""
    try:
        # 模型API調用邏輯
        response = call_new_model_api(requirement)
        
        return {
            "analysis": parse_response(response),
            "confidence": 0.8,
            "next_steps": ["步驟1", "步驟2"]
        }
    except Exception as e:
        return error_response(e)
```

2. **在路由器中添加模型選項**
```python
elif selected_model == 'new_model':
    analysis_result = analyze_with_new_model(requirement)
```

3. **在UI中添加選項**
```html
<option value="new_model">新模型</option>
```

### 添加新文件格式支持

1. **更新允許的文件擴展名**
```python
ALLOWED_EXTENSIONS.add('new_extension')
```

2. **添加文件處理邏輯**
```python
def process_new_format(file_path):
    """處理新格式文件"""
    # 文件解析邏輯
    return extracted_content
```

### 性能優化建議

1. **緩存機制**
   - 實現結果緩存
   - 模型響應緩存
   - 文件處理緩存

2. **異步處理**
   - 使用異步框架
   - 後台任務隊列
   - 流式響應

3. **負載平衡**
   - 多實例部署
   - 模型負載分散
   - 數據庫讀寫分離

## 故障排除

### 常見問題

#### 1. 模型API調用失敗
- 檢查API密鑰配置
- 驗證網絡連接
- 查看API限制

#### 2. 文件上傳失敗
- 檢查文件大小限制
- 驗證文件格式支持
- 查看磁盤空間

#### 3. 響應時間過長
- 優化模型選擇
- 實現結果緩存
- 調整超時設置

### 日誌分析
```bash
# 查看服務日誌
tail -f logs/service.log

# 查看錯誤日誌
grep ERROR logs/service.log

# 查看性能日誌
grep "response_time" logs/service.log
```

