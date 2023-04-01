from django.db import models

# Create your models here.
class Document(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField()

class TranscriptResult(models.Model):
    status = models.CharField(max_length=50, default="None")
    audio_info = models.DecimalField(max_digits=24, decimal_places=3, default=0)
    transcribe_result = models.TextField(default="None")
    translate_result = models.TextField(default="None")
    sentiment_result = models.CharField(max_length=500, default="None")

class TemporaryAudio(models.Model):
    audio = models.FileField(upload_to='audio/')