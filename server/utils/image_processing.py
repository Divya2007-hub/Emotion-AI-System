import base64
import numpy as np
import cv2
import os
from django.conf import settings


def decode_base64_image(base64_string):
    try:
        image_data = base64.b64decode(base64_string)
        np_arr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return image
    except Exception as e:
        print("Decode error:", e)
        return None


def detect_face(image):
    try:
        cascade_path = os.path.join(settings.BASE_DIR, 'haarcascade_frontalface_default.xml')
        face_cascade = cv2.CascadeClassifier(cascade_path)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        if len(faces) == 0:
            return None

        x, y, w, h = faces[0]  # Take first face
        face = gray[y:y+h, x:x+w]

        return face

    except Exception as e:
        print("Face detection error:", e)
        return None


def preprocess_face(face, target_size):
    try:
        face = cv2.resize(face, target_size)

        face = face / 255.0  # normalize

        face = np.reshape(face, (1, target_size[0], target_size[1], 1))

        return face

    except Exception as e:
        print("Preprocess error:", e)
        return None