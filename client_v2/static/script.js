const video = document.getElementById("video");

function showScreen(id) {
    document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
    document.getElementById(id).classList.add("active");
}

async function startCapture() {
    // getUserMedia only exists in a secure context (http://127.0.0.1, http://localhost, or https)
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert("Camera API unavailable. Open the page at http://127.0.0.1:7000 or over https (a secure context is required).");
        return;
    }

    try {
        // Ask permission (user can select OBS camera here)
        const stream = await navigator.mediaDevices.getUserMedia({
            video: true
        });

        video.srcObject = stream;
        await video.play().catch(() => {});

        showScreen("loading-screen");

        // wait for the camera to actually deliver frames
        await waitForVideoReady();
        captureImage();

    } catch (err) {
        alert("Camera error: " + err.name + " - " + err.message);
    }
}

function waitForVideoReady() {
    return new Promise((resolve) => {
        const check = () => {
            if (video.readyState >= 2 && video.videoWidth > 0) {
                resolve();
            } else {
                setTimeout(check, 100);
            }
        };
        check();
    });
}

function captureImage() {
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    const base64 = canvas.toDataURL("image/jpeg").split(',')[1];

    sendToServer(base64);
}

async function sendToServer(image) {
    try {
        const res = await fetch("http://127.0.0.1:8000/api/predict/", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ image })
        });

        const data = await res.json();

        showResult(data);

    } catch (err) {
        alert("Server error");
    }
}

function showResult(data) {
    showScreen("result-screen");

    if (data.error) {
        document.getElementById("emotion-text").innerText = "Error";
        return;
    }

    const emotion = data.emotion;

    document.getElementById("emotion-text").innerText = emotion;

    const gifs = {
        "Happy": "gifs/happy.gif",
        "Sad": "gifs/sad.gif",
        "Angry": "gifs/angry.gif",
        "Surprise": "gifs/surprise.gif",
        "Neutral": "gifs/neutral.gif"
    };

    document.getElementById("emotion-gif").src = gifs[emotion] || "";
}

function reset() {
    showScreen("start-screen");
}