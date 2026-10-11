const video = document.getElementById("video");

function showScreen(id) {
    document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
    document.getElementById(id).classList.add("active");
}

async function startApp() {
    try {
        const devices = await navigator.mediaDevices.enumerateDevices();

        const videoDevices = devices.filter(d => d.kind === "videoinput");

        let deviceId = videoDevices[0].deviceId;

        // Ask camera permission + allow selection
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { deviceId: deviceId }
        });

        video.srcObject = stream;

        showScreen("camera-screen");

    } catch (err) {
        alert("Camera permission required");
    }
}

function capture() {
    showScreen("loading-screen");

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    const image = canvas.toDataURL("image/jpeg").split(',')[1];

    sendToServer(image);
}

async function sendToServer(image) {
    const res = await fetch("http://127.0.0.1:8000/api/predict/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image })
    });

    const data = await res.json();

    showResult(data);
}

function showResult(data) {
    showScreen("result-screen");

    if (data.error) {
        document.getElementById("emotion-text").innerText = "Error";
        return;
    }

    const emotion = data.emotion;

    document.getElementById("emotion-text").innerText = emotion;

    const gifMap = {
        "Happy": "gifs/happy.gif",
        "Sad": "gifs/sad.gif",
        "Angry": "gifs/angry.gif",
        "Surprise": "gifs/surprise.gif",
        "Neutral": "gifs/neutral.gif"
    };

    document.getElementById("emotion-gif").src = gifMap[emotion] || "";
}