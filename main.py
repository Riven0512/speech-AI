from fastapi import FastAPI, WebSocket
from google.cloud import speech
import os

app = FastAPI()

# 初始化 Google Speech-to-Text 客戶端
client = speech.SpeechClient()

@app.websocket("/transcribe")
async def transcribe_audio(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            # 接收音頻數據
            audio_data = await websocket.receive_bytes()

            # 配置語音識別
            audio = speech.RecognitionAudio(content=audio_data)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="en-US",  # 可更改為其他語言代碼
            )

            # 呼叫 Google Speech-to-Text API
            response = client.recognize(config=config, audio=audio)

            # 傳回識別結果
            for result in response.results:
                await websocket.send_text(result.alternatives[0].transcript)

        except Exception as e:
            await websocket.send_text(f"Error: {str(e)}")
            break
