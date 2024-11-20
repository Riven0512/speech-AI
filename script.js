document.getElementById("uploadForm").addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData();
  formData.append("language", document.getElementById("language").value);
  formData.append("file", document.getElementById("audioFile").files[0]);

  const resultDiv = document.getElementById("result");
  const transcriptionEl = document.getElementById("transcription");
  const summaryEl = document.getElementById("summary");

  resultDiv.style.display = "none";
  transcriptionEl.textContent = "Loading...";
  summaryEl.textContent = "Loading...";

  try {
    const response = await fetch("https://<your-backend-url>/transcribe", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    if (response.ok) {
      transcriptionEl.textContent = data.transcription;
      summaryEl.textContent = data.summary;
    } else {
      transcriptionEl.textContent = "Error: " + data.error;
      summaryEl.textContent = "";
    }
  } catch (error) {
    transcriptionEl.textContent = "Error: " + error.message;
    summaryEl.textContent = "";
  }

  resultDiv.style.display = "block";
});
