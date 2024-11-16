from flask import Flask, request, jsonify
from flask_cors import CORS  # 导入 CORS 扩展
import speech_recognition as sr

app = Flask(__name__)

# 启用 CORS，允许所有源访问
CORS(app)

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio_file']
    
    # 保存音频文件到本地
    audio_path = 'uploaded_audio.wav'
    audio_file.save(audio_path)

    # 使用 SpeechRecognition 进行转录
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)  # 读取音频

    try:
        transcription = recognizer.recognize_google(audio, language='zh-TW')  # 使用 Google 的语音识别
        return jsonify({'transcription': transcription})
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'}), 500
    except sr.RequestError as e:
        return jsonify({'error': f'Speech recognition service error: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    return jsonify({'message': 'Processed successfully', 'data': data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

