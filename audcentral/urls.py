from django.urls import path

from . import views

app_name = 'audcentral'

urlpatterns = [
    path('', views.main, name='base'),
    path('top-tracks-region', views.getTopTrackRegion, name='base'),
    path('top-tracks-region/<req>', views.getTopTrackRegionDataFormat, name='base'),
    path('identify-track', views.identifyTrackUpload, name='base'),
    path('identify-track/json', views.identifyTrackUploadJSON, name='base'),
]