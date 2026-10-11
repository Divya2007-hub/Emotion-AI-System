
import os
import tensorflow as tf
from django.conf import settings
from api.models import EmotionModel

# Global cache
model = None
input_size = None
loaded_model_id = None


def load_active_model():
    """
    Load the active model configured in Django admin.

    If no active database record exists, fall back to the
    bundled model2.h5 file.
    """
    global model, input_size, loaded_model_id

    try:
        active_model = EmotionModel.objects.filter(
            is_active=True
        ).first()

        if active_model:
            model_path = os.path.join(
                settings.MEDIA_ROOT,
                active_model.model_file.name
            )
            current_model_id = active_model.id
        else:
            # Fallback for fresh deployments without a database record.
            model_path = os.path.join(
                settings.BASE_DIR,
                "models_storage",
                "models",
                "model2.h5"
            )
            current_model_id = "default-model2"

        if not os.path.isfile(model_path):
            print(f"Model file not found: {model_path}")
            return None, None

        # Reuse the cached model when it has not changed.
        if (
            loaded_model_id == current_model_id
            and model is not None
        ):
            return model, input_size

        print(f"Loading emotion model: {model_path}")

        loaded_model = tf.keras.models.load_model(model_path)

        model_input_shape = loaded_model.input_shape
        loaded_input_size = model_input_shape[1:3]

        model = loaded_model
        input_size = loaded_input_size
        loaded_model_id = current_model_id

        print(f"Model ready. Input size: {input_size}")

        return model, input_size

    except Exception as e:
        print(f"Model load error: {e}")
        return None, None
