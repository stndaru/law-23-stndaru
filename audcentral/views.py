from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from .models import Document
import json, requests, mutagen
from django.views.decorators.csrf import csrf_exempt

LASTFM_TOKEN = "14e1db88026c7814d4ed01afac4f1e6b"
AUD_TOKEN = "52d936452cec3fa3b2127034a38febc6" # Expire 24 March

# Create your views here.
def main(request):
    return render(request, 'index.html')


def identifyTrackUpload(request):

    status = "Error"

    if request.method=="POST":

        if request.FILES["audio"]:
            audio = request.FILES["audio"]

            audio_info = mutagen.File(audio).info

            if audio_info.length < 20 and audio.size < 19971520:
                status = "Success"

        return render(request, "identifyTrack.html", {"audio_info":audio_info, "status": status})
    
    return render(request, "identifyTrack.html")

@csrf_exempt
def identifyTrackUploadJSON(request):

    status = "Error"
    audio_info = "None"

    if request.method=="POST":

        validity = request.POST.get('audio', False)
        
        if validity:
            audio = request.FILES["audio"]

            audio_info = mutagen.File(audio).info

            if audio_info.length < 20 and audio.size < 19971520:
                status = "Success"

        context = {
            audio_info : audio_info,
            status: status,
        }

        return HttpResponse(json.dumps(context), content_type="application/json")
    
    return HttpResponseBadRequest



def getTopTrackRegion(request):
    country_id = "spain"
    response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country={country_id}&api_key={LASTFM_TOKEN}&format=json")

    json_data = json.loads(response.text)

    return render(request, 'topTracks.html', {'result': json_data})


def getTopTrackRegionDataFormat(request, req):
    country_id = "spain"
    response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country={country_id}&api_key={LASTFM_TOKEN}&format=json")
    data = json.loads(response.text)

    print(data)
    
    if req == "JSON":
        # TODO
        return HttpResponse(json.dumps(data), content_type="application/json")
    
    elif req == "" or None:
        return HttpResponseRedirect("")
    
    else:
        return HttpResponseBadRequest