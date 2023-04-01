from django.contrib import admin
from .models import TranscriptResult, TemporaryAudio

# Register your models here.
admin.site.register(TranscriptResult)
admin.site.register(TemporaryAudio)