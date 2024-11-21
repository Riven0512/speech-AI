from fastapi import FastAPI, WebSocket
from google.cloud import speech
import json

app = FastAPI()

# 初始化 Google Speech-to-Text 客戶端
client = speech.SpeechClient()

@app.websocket("/transcribe")
async def transcribe_audio(websocket: WebSocket):
    await websocket.accept()
    
    # 首先接收語言代碼
    language_code = await websocket.receive_text()

    while True:
        try:
            # 接收音頻數據
            audio_data = await websocket.receive_bytes()

            # 配置語音識別
            audio = speech.RecognitionAudio(content=audio_data)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=language_code,  # 使用動態語言代碼
            )

            # 呼叫 Google Speech-to-Text API
            response = client.recognize(config=config, audio=audio)

            # 傳回識別結果
            for result in response.results:
                await websocket.send_text(result.alternatives[0].transcript)

        except Exception as e:
            await websocket.send_text(json.dumps({"error": str(e)}))
            break
