# Ollama Setup Guide for Vietnam Stock Analyzer

## 🚀 Cài đặt Ollama

### Bước 1: Cài đặt Ollama
**Windows:**
1. Tải Ollama từ: https://ollama.com/download
2. Chạy file `.exe` đã tải
3. Khởi động lại terminal sau khi cài đặt

### Bước 2: Kiểm tra cài đặt
```bash
ollama --version
```

### Bước 3: Pull Model Llama3
```bash
ollama pull llama3
```

Hoặc sử dụng model nhẹ hơn:
```bash
ollama pull llama3:8b
```

### Bước 4: Kiểm tra model đã có
```bash
ollama list
```

### Bước 5: Khởi động Ollama server
```bash
ollama serve
```

## 🔧 Cấu hình cho Vietnam Stock Analyzer

### Môi trường variables (tùy chọn)
Nếu muốn thay đổi model mặc định:
```bash
set OLLAMA_MODEL=llama3:8b
set OLLAMA_BASE_URL=http://localhost:11434
```

## 📝 Model đề xuất

### Cho máy tính yếu:
- `llama3:8b` - 4.7GB
- `qwen:7b` - 4.1GB
- `phi3` - 2.2GB

### Cho máy tính mạnh:
- `llama3` - 4.7GB
- `codellama` - 3.8GB
- `mistral` - 4.1GB

## 🐛 Troubleshooting

### Lỗi 404 Model not found:
```bash
# Kiểm tra model có sẵn
ollama list

# Pull model nếu chưa có
ollama pull llama3:8b
```

### Lỗi kết nối:
```bash
# Kiểm tra Ollama server đang chạy
ollama serve

# Kiểm tra port 11434
curl http://localhost:11434/api/tags
```

### Lỗi memory:
- Sử dụng model nhỏ hơn: `qwen:7b` hoặc `phi3`
- Tăng RAM hoặc đóng các ứng dụng khác

## 🎯 Sử dụng với Vietnam Stock Analyzer

Sau khi cài đặt xong:
1. Khởi động Ollama server: `ollama serve`
2. Khởi động backend Python
3. Frontend sẽ tự động kết nối đến Ollama

Multi-agent system sẽ sử dụng Ollama cho:
- Market analysis
- Technical analysis  
- News sentiment analysis
- Risk assessment
- Final decision making
