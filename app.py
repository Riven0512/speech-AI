from flask import Flask, request, jsonify
from flask_cors import CORS  # 导入 CORS 扩展
import speech_recognition as sr
import logging

app = Flask(__name__)

# 启用 CORS，允许所有源访问
CORS(app)

# 设置日志记录
logging.basicConfig(level=logging.DEBUG)

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio_file' not in request.files:
        app.logger.error("No audio file provided")
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio_file']
    
    # 保存音频文件到本地
    audio_path = 'uploaded_audio.wav'
    audio_file.save(audio_path)

    # 使用 SpeechRecognition 进行转录
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)  # 读取音频
        transcription = recognizer.recognize_google(audio, language='zh-TW')  # 使用 Google 的语音识别
        return jsonify({'transcription': transcription})
    except sr.UnknownValueError:
        app.logger.error("Could not understand the audio")
        return jsonify({'error': 'Could not understand audio'}), 500
    except sr.RequestError as e:
        app.logger.error(f"Speech recognition service error: {e}")
        return jsonify({'error': f'Speech recognition service error: {e}'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
