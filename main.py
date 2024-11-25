from fastapi import FastAPI, WebSocket
from google.cloud import speech
import json

app = FastAPI()


client = speech.SpeechClient()

@app.websocket("/transcribe")
async def transcribe_audio(websocket: WebSocket):
    await websocket.accept()
    
   
    language_code = await websocket.receive_text()

    while True:
        try:
            audio_data = await websocket.receive_bytes()
        
            audio = speech.RecognitionAudio(content=audio_data)
            config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,sample_rate_hertz=16000,language_code=language_code, )

           
            response = client.recognize(config=config, audio=audio)

           
            for result in response.results:
                await websocket.send_text(result.alternatives[0].transcript)

        except Exception as e:
            await websocket.send_text(json.dumps({"error": str(e)}))
            break
