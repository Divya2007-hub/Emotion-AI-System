import os
import tensorflow as tf
from django.conf import settings
from api.models import EmotionModel

# Global cache
model = None
input_size = None
loaded_model_id = None


def load_active_model():
    global model, input_size, loaded_model_id

    try:
        active_model = EmotionModel.objects.filter(is_active=True).first()

        if not active_model:
            print("No active model found")
            return None, None

        # 🔥 Reload only if model changed
        if loaded_model_id == active_model.id and model is not None:
            return model, input_size

        model_path = os.path.join(settings.MEDIA_ROOT, active_model.model_file.name)

        print(f"Loading NEW model: {model_path}")

        model = tf.keras.models.load_model(model_path)

        input_shape = model.input_shape
        input_size = input_shape[1:3]

        loaded_model_id = active_model.id

        print(f"Model ready. Input size: {input_size}")

        return model, input_size

    except Exception as e:
        print("Model load error:", e)
        return None, None