from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr

app = Flask(__name__)
CORS(app)  # 啟用 CORS，允許跨域請求

# 處理語音上傳與轉錄
@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio_file']
    audio_path = 'uploaded_audio.wav'  # 保存到本地
    audio_file.save(audio_path)

    # 使用 SpeechRecognition 進行轉錄
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        transcription = recognizer.recognize_google(audio, language='zh-TW')
        return jsonify({'transcription': transcription})
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'}), 500
    except sr.RequestError as e:
        return jsonify({'error': f'Speech recognition service error: {e}'}), 500

# 處理 JSON 數據
@app.route('/process', methods=['POST'])
def process():
    data = request.json
    return jsonify({'message': 'Processed successfully', 'data': data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
