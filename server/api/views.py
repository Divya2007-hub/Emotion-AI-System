from rest_framework.decorators import api_view
from rest_framework.response import Response

from utils.model_loader import load_active_model
from utils.image_processing import decode_base64_image, detect_face, preprocess_face

import numpy as np
import psutil

@api_view(['GET'])
def system_status(request):
    return Response({
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent
    })


# Emotion labels (CHANGE if your model differs)
EMOTIONS = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]


@api_view(['GET'])
def health_check(request):
    return Response({
        "status": "OK",
        "message": "Server is running"
    })


@api_view(['POST'])
def predict_emotion(request):
    try:
        base64_image = request.data.get("image")

        if not base64_image:
            return Response({"error": "No image provided"}, status=400)

        # Decode
        image = decode_base64_image(base64_image)
        if image is None:
            return Response({"error": "Invalid image"}, status=400)

        # Detect face
        face = detect_face(image)
        if face is None:
            return Response({"error": "No face detected"}, status=400)

        # Load model
        model, input_size = load_active_model()
        if model is None:
            return Response({"error": "Model not loaded"}, status=500)

        # Preprocess
        processed = preprocess_face(face, input_size)
        if processed is None:
            return Response({"error": "Preprocessing failed"}, status=500)

        # Predict
        predictions = model.predict(processed, verbose=0)
        emotion_index = np.argmax(predictions)
        confidence = float(np.max(predictions))

        emotion = EMOTIONS[emotion_index]

        return Response({
            "emotion": emotion,
            "confidence": confidence
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)