import os
import whisper
import speech_recognition as sr
from flask import Flask, request, jsonify, render_template
from pydub import AudioSegment
from io import BytesIO

app = Flask(__name__)

# 初始化 Whisper 模型
model = whisper.load_model("base")

# 設定語音識別
recognizer = sr.Recognizer()

# 錄音保存的目錄
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 錄音並將其保存為音檔
def save_audio_from_bytes(audio_bytes):
    file_path = os.path.join(UPLOAD_FOLDER, 'recorded_audio.wav')
    with open(file_path, 'wb') as f:
        f.write(audio_bytes)
    return file_path

# 使用 Whisper 進行語音識別並返回文本
def transcribe_audio(file_path):
    try:
        result = model.transcribe(file_path)
        return result['text']
    except Exception as e:
        print(f"語音轉錄錯誤: {e}")
        return None

# 網頁首頁路由
@app.route('/')
def index():
    return render_template('index.html')

# 用於處理上傳音檔的路由
@app.route('/process_audio', methods=['POST'])
def process_audio():
    audio_file = request.files['audio_file']
    audio_bytes = audio_file.read()

    file_path = save_audio_from_bytes(audio_bytes)
    transcription = transcribe_audio(file_path)

    if transcription:
        # 在這裡進行分析，這裡只是進行簡單的顯示
        analysis = {'transcription': transcription}
        return jsonify({'message': '轉錄成功', 'transcription': transcription, 'analysis': analysis})
    else:
        return jsonify({'error': '語音轉錄失敗'}), 500

if __name__ == "__main__":
    app.run(debug=True)
