from django.db import models


class EmotionModel(models.Model):
    name = models.CharField(max_length=100)
    model_file = models.FileField(upload_to='models/')
    is_active = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            EmotionModel.objects.update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name