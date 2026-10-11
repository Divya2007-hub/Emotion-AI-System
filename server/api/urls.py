from django.urls import path
from .views import health_check, predict_emotion, system_status

urlpatterns = [
    path('health/', health_check),
    path('predict/', predict_emotion),
    path('status/', system_status),
]