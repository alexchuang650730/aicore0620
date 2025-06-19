# 多模態需求分析系統測試

## 測試用例

### 1. 基本功能測試

#### 健康檢查測試
```bash
curl http://localhost:8300/health
```

#### API信息測試
```bash
curl http://localhost:8300/api/info
```

### 2. 需求分析測試

#### MiniMax模型測試
```bash
curl -X POST http://localhost:8300/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "requirement": "我想開發一個線上購物網站，需要支援用戶註冊、商品瀏覽、購物車和支付功能",
    "model": "minimax"
  }'
```

#### Gemini Flash測試
```bash
curl -X POST http://localhost:8300/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "requirement": "開發一個企業內部的文檔管理系統",
    "model": "gemini_flash"
  }'
```

#### Claude Sonnet測試
```bash
curl -X POST http://localhost:8300/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "requirement": "設計一個智能客服聊天機器人",
    "model": "claude_sonnet"
  }'
```

### 3. 文檔上傳測試

#### PDF文檔測試
```bash
curl -X POST http://localhost:8300/api/upload-document \
  -F "file=@test_document.pdf" \
  -F "model=minimax"
```

#### 圖片OCR測試
```bash
curl -X POST http://localhost:8300/api/upload-document \
  -F "file=@test_image.png" \
  -F "model=gemini_flash"
```

### 4. 性能測試

#### 響應時間測試
```bash
time curl -X POST http://localhost:8300/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"requirement": "簡單的網站需求", "model": "auto"}'
```

#### 並發測試
```bash
# 使用ab工具進行並發測試
ab -n 100 -c 10 -T 'application/json' \
  -p test_data.json \
  http://localhost:8300/api/analyze
```

## 測試數據

### 測試需求樣本
1. "開發一個電商網站"
2. "設計一個移動應用程式"
3. "建立一個數據分析平台"
4. "創建一個社交媒體平台"
5. "開發一個在線教育系統"

### 預期結果
- 響應時間 < 5秒
- 分析置信度 > 0.7
- 結構化JSON輸出
- 繁體中文支持

## 測試報告模板

### 功能測試結果
- [ ] 健康檢查正常
- [ ] API信息完整
- [ ] MiniMax模型正常
- [ ] Gemini模型正常
- [ ] Claude模型正常
- [ ] 文檔上傳正常
- [ ] 繁體中文輸出正確

### 性能測試結果
- 平均響應時間: ___ms
- 最大響應時間: ___ms
- 並發處理能力: ___req/s
- 錯誤率: ___%

