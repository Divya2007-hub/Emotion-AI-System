import cv2
import requests
import base64
import time
import os
import webbrowser

# ================= CONFIG =================
API_URL = "http://127.0.0.1:8000/api/predict/"
UI_URL = "http://127.0.0.1:5500"   # IMPORTANT (NOT file://)

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


# ================= CAMERA =================
def capture_face():
    cap = cv2.VideoCapture(0)

    time.sleep(2)  # Camera warmup

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("❌ Camera error")
        return None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    if len(faces) == 0:
        print("❌ No face detected")
        return None

    x, y, w, h = faces[0]
    face = frame[y:y+h, x:x+w]

    return face


# ================= IMAGE =================
def encode_image(image):
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')


# ================= API =================
def send_to_server(base64_image):
    try:
        response = requests.post(API_URL, json={"image": base64_image})
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# ================= MAIN =================
def main():
    # Open UI in browser (HTTP server)
    print("Opening UI...")
    webbrowser.open(UI_URL)

    result_path = os.path.join("ui", "result.txt")

    # Ensure file exists
    if not os.path.exists(result_path):
        with open(result_path, "w") as f:
            f.write("")

    # Clear previous result
    with open(result_path, "w") as f:
        f.write("")

    print("Capturing face...")
    face = capture_face()

    if face is None:
        print("❌ Failed to capture face")
        return

    print("Sending to server...")
    img_base64 = encode_image(face)

    result = send_to_server(img_base64)

    print("API Response:", result)

    # Write result to file
    try:
        with open(result_path, "w") as f:
            if "emotion" in result:
                f.write(result["emotion"])
                print("✅ Emotion written:", result["emotion"])
            else:
                f.write("Error")
                print("❌ Error writing result")
    except Exception as e:
        print("❌ File write error:", e)


if __name__ == "__main__":
    main()