import whisper
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from transformers import pipeline
import os

app = FastAPI()

# 加載 Whisper 模型
whisper_model = whisper.load_model("base")
# 加載 Hugging Face 摘要模型
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# 定義返回格式
class TranscriptionResponse(BaseModel):
    transcription: str
    summary: str

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(file: UploadFile = File(...), language: str = Form("en")):
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as f:
        f.write(file.file.read())
    
    try:
        # Whisper 語音轉文字
        transcription_result = whisper_model.transcribe(temp_file, language=language)
        transcription = transcription_result["text"]
        
        # 生成摘要
        summary = summarizer(transcription, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    return TranscriptionResponse(transcription=transcription, summary=summary)
