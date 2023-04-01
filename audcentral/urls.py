from django.urls import path

from . import views

app_name = 'audcentral'

urlpatterns = [
    path('', views.main, name='base'),
    
    path('top-tracks-region/<country>', views.getTopTrackRegion, name='base'),
    path('top-tracks-region/json/<country>', views.getTopTrackRegionJSON, name='base'),

    path('identify-track', views.identifyTrackUpload, name='base'),
    path('identify-track/json', views.identifyTrackUploadJSON, name='base'),

    path('search-name/json/<name>', views.getTrackDetailsJSON, name='base'),
    path('random/json', views.randomSongJSON),

    path('transcribe-text', views.transcribeText),
    path('transcribe-text/<id>', views.transcribeTextView)
]