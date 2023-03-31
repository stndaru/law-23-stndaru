from django.db import models

# Create your models here.
class Document(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField()

class TranscriptResult(models.Model):
    transcribe_result = models.TextField()
    translate_result = models.TextField()
    sentiment_result = models.CharField(max_length=500)