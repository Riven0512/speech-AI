# 基於 Python 3.11 Slim 映像構建
FROM python:3.11-slim

# 安裝必要的系統依賴 (這裡安裝 portaudio 依賴，適用於 pyaudio)
RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製本地應用程式代碼到容器中
COPY . /app

# 安裝應用程式的 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 容器啟動時運行的命令，通常是啟動 Flask 應用
CMD ["python", "app.py"]
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
