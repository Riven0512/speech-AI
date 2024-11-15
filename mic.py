from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    return jsonify({'message': 'Processed successfully', 'data': data})

if __name__ == '__main__':
    app.run(debug=False)
