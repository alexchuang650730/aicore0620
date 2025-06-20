# AWS EC2 部署指導 - 純AI驅動分析系統

**目標目錄**: `/opt/aiengine/`  
**服務名稱**: `aiengine`  
**端口**: `8300`

---

## 🚀 快速部署步驟

### 1. 連接到EC2實例
```bash
ssh -i alexchuang.pem ec2-user@18.212.97.173
```

### 2. 上傳部署文件
```bash
# 在本地機器上執行
scp -i alexchuang.pem ec2_deploy.sh ec2-user@18.212.97.173:~/
scp -i alexchuang.pem production_service.py ec2-user@18.212.97.173:~/
scp -i alexchuang.pem fully_dynamic_ai_engine.py ec2-user@18.212.97.173:~/
```

### 3. 執行部署腳本
```bash
# 在EC2實例上執行
chmod +x ec2_deploy.sh
./ec2_deploy.sh
```

### 4. 移動文件到目標目錄
```bash
sudo mv ~/production_service.py /opt/aiengine/
sudo mv ~/fully_dynamic_ai_engine.py /opt/aiengine/
sudo chown ec2-user:ec2-user /opt/aiengine/*
```

### 5. 創建日誌目錄
```bash
sudo mkdir -p /opt/aiengine/logs
sudo chown ec2-user:ec2-user /opt/aiengine/logs
```

### 6. 啟動服務
```bash
sudo systemctl start aiengine
sudo systemctl status aiengine
```

---

## 📋 詳細部署流程

### 階段1: 環境準備

#### 1.1 系統更新
```bash
sudo yum update -y
sudo yum groupinstall -y "Development Tools"
sudo yum install -y git curl wget vim htop
```

#### 1.2 Python 3.11 安裝
```bash
# 安裝基礎Python
sudo yum install -y python3 python3-pip python3-devel

# 如需Python 3.11，從源碼編譯
cd /tmp
wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz
tar xzf Python-3.11.0.tgz
cd Python-3.11.0
sudo yum install -y openssl-devel libffi-devel bzip2-devel
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall
```

#### 1.3 創建目錄結構
```bash
sudo mkdir -p /opt/aiengine
sudo mkdir -p /opt/aiengine/logs
sudo chown ec2-user:ec2-user /opt/aiengine
sudo chown ec2-user:ec2-user /opt/aiengine/logs
```

### 階段2: 依賴安裝

#### 2.1 Python依賴
```bash
pip3 install --user flask flask-cors aiohttp asyncio python-multipart
```

#### 2.2 系統依賴
```bash
sudo yum install -y nginx  # 可選：反向代理
```

### 階段3: 應用部署

#### 3.1 文件部署
```bash
# 複製核心文件到目標目錄
cp ~/production_service.py /opt/aiengine/
cp ~/fully_dynamic_ai_engine.py /opt/aiengine/
```

#### 3.2 權限設置
```bash
chmod +x /opt/aiengine/production_service.py
chown -R ec2-user:ec2-user /opt/aiengine/
```

### 階段4: 服務配置

#### 4.1 systemd服務文件
```bash
sudo tee /etc/systemd/system/aiengine.service > /dev/null <<EOF
[Unit]
Description=AI Engine Analysis System
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/opt/aiengine
Environment=PATH=/usr/local/bin:/usr/bin:/bin
ExecStart=/usr/bin/python3 production_service.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

#### 4.2 啟用服務
```bash
sudo systemctl daemon-reload
sudo systemctl enable aiengine
sudo systemctl start aiengine
```

### 階段5: 網絡配置

#### 5.1 防火牆配置
```bash
# CentOS/RHEL/Amazon Linux
sudo firewall-cmd --permanent --add-port=8300/tcp
sudo firewall-cmd --reload

# 或者使用iptables
sudo iptables -A INPUT -p tcp --dport 8300 -j ACCEPT
sudo service iptables save
```

#### 5.2 AWS安全組配置
在AWS控制台中：
1. 進入EC2 → 安全組
2. 選擇實例的安全組
3. 添加入站規則：
   - 類型：自定義TCP
   - 端口：8300
   - 來源：0.0.0.0/0 (或指定IP範圍)

---

## 🔧 服務管理命令

### 基本操作
```bash
# 啟動服務
sudo systemctl start aiengine

# 停止服務
sudo systemctl stop aiengine

# 重啟服務
sudo systemctl restart aiengine

# 查看狀態
sudo systemctl status aiengine

# 查看日誌
sudo journalctl -u aiengine -f

# 查看應用日誌
tail -f /opt/aiengine/logs/ai-analysis.log
```

### 故障排除
```bash
# 檢查端口占用
netstat -tlnp | grep 8300

# 檢查進程
ps aux | grep python

# 測試本地連接
curl http://localhost:8300/health

# 測試外部連接
curl http://18.212.97.173:8300/health
```

---

## 📊 監控和維護

### 日誌監控
```bash
# 實時查看服務日誌
sudo journalctl -u aiengine -f

# 查看應用日誌
tail -f /opt/aiengine/logs/ai-analysis.log

# 查看錯誤日誌
grep ERROR /opt/aiengine/logs/ai-analysis.log
```

### 性能監控
```bash
# 查看系統資源
htop

# 查看內存使用
free -h

# 查看磁盤使用
df -h

# 查看網絡連接
netstat -an | grep 8300
```

### 自動備份
```bash
# 創建備份腳本
sudo tee /opt/aiengine/backup.sh > /dev/null <<EOF
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf /opt/aiengine/backup/aiengine_backup_\$DATE.tar.gz /opt/aiengine/*.py /opt/aiengine/logs/
find /opt/aiengine/backup/ -name "*.tar.gz" -mtime +7 -delete
EOF

chmod +x /opt/aiengine/backup.sh

# 添加到crontab
echo "0 2 * * * /opt/aiengine/backup.sh" | sudo crontab -
```

---

## 🌐 訪問測試

### 健康檢查
```bash
curl http://18.212.97.173:8300/health
```

### API測試
```bash
curl -X POST http://18.212.97.173:8300/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "requirement": "測試需求：核保流程分析",
    "model": "fully_dynamic_ai_engine"
  }'
```

### 瀏覽器訪問
```
http://18.212.97.173:8300
```

---

## ⚠️ 注意事項

### 安全考慮
1. **防火牆配置**：確保只開放必要的端口
2. **SSL證書**：生產環境建議配置HTTPS
3. **訪問控制**：考慮添加身份驗證
4. **日誌輪轉**：配置日誌輪轉避免磁盤滿

### 性能優化
1. **反向代理**：使用Nginx作為反向代理
2. **負載均衡**：多實例部署時配置負載均衡
3. **緩存機制**：添加Redis緩存提高響應速度
4. **監控告警**：配置CloudWatch監控

### 維護建議
1. **定期更新**：定期更新系統和依賴包
2. **備份策略**：定期備份應用和數據
3. **監控告警**：設置服務異常告警
4. **文檔更新**：及時更新部署文檔

---

## 🎯 部署檢查清單

- [ ] EC2實例可正常連接
- [ ] 系統更新完成
- [ ] Python 3.11安裝成功
- [ ] 目錄 `/opt/aiengine/` 創建完成
- [ ] Python依賴安裝完成
- [ ] 應用文件上傳完成
- [ ] systemd服務配置完成
- [ ] 防火牆端口開放
- [ ] AWS安全組配置完成
- [ ] 服務啟動成功
- [ ] 健康檢查通過
- [ ] API測試成功
- [ ] 瀏覽器訪問正常
- [ ] 日誌記錄正常
- [ ] 監控配置完成

完成以上檢查清單後，您的純AI驅動分析系統就成功部署到AWS EC2的 `/opt/aiengine/` 目錄了！

