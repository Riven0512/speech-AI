document.getElementById('transcribeButton').addEventListener('click', async () => {
    const audioFile = document.getElementById('audio').files[0];
    const language = document.getElementById('language').value;

    if (!audioFile) {
        alert("請上傳語音檔案！");
        return;
    }

    const formData = new FormData();
    formData.append("file", audioFile);
    formData.append("language", language);

    try {
        // 調用後端 API 進行轉錄
        const response = await fetch("https://<你的後端域名>/transcribe", {
            method: "POST",
            body: formData,
        });
        const data = await response.json();

        document.getElementById('transcript').textContent = data.transcription || "轉錄失敗！";
        document.getElementById('summary').textContent = data.summary || "摘要生成失敗！";
    } catch (error) {
        console.error("發生錯誤：", error);
        alert("無法處理請求！");
    }
});
