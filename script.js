const languageSelect = document.getElementById("languageSelect");
const startButton = document.getElementById("startButton");
let websocket;

startButton.addEventListener("click", () => {const languageCode = languageSelect.value;const serverURL = "wss://<your-render-url>/transcribe"; websocket = new WebSocket(serverURL);

    websocket.onopen = () => {console.log("WebSocket connected");websocket.send(languageCode);};

    websocket.onmessage = (event) => {const transcription = document.getElementById("transcription");
        try {const data = JSON.parse(event.data);if (data.error) {transcription.innerText += `Error: ${data.error}\n`;}} catch {transcription.innerText += event.data + "\n";};

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then((stream) => {const audioContext = new AudioContext();const mediaRecorder = audioContext.createScriptProcessor(4096, 1, 1);const source = audioContext.createMediaStreamSource(stream);

            source.connect(mediaRecorder);
            mediaRecorder.connect(audioContext.destination);

            mediaRecorder.onaudioprocess = (event) => {const audioData = event.inputBuffer.getChannelData(0);const int16Array = new Int16Array(audioData.map((n) => n * 0x7FFF));websocket.send(int16Array);};}).catch((err) => {console.error("Error accessing microphone:", err);});});
