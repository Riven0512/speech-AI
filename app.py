from flask import Flask, request, jsonify
from flask_cors import CORS  # 导入 CORS 扩展
import speech_recognition as sr
import os

app = Flask(__name__)

# 启用 CORS，允许所有源访问
CORS(app)

# 設置音頻保存的路徑
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/process_audio', methods=['POST'])
def process_audio():
    # 確認是否包含音頻文件
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio_file']
    
    # 保存音頻文件
    audio_path = os.path.join(UPLOAD_FOLDER, 'uploaded_audio.wav')
    audio_file.save(audio_path)

    # 使用 SpeechRecognition 進行語音轉錄
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)  # 读取音频

    try:
        transcription = recognizer.recognize_google(audio, language='zh-TW')  # 使用 Google 語音識別
        return jsonify({'transcription': transcription})
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'}), 500
    except sr.RequestError as e:
        return jsonify({'error': f'Speech recognition service error: {e}'}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
