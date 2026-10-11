from django.contrib import admin
from .models import EmotionModel


@admin.register(EmotionModel)
class EmotionModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'uploaded_at')