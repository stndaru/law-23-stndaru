from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from .models import Document
import json, requests, mutagen, random
from django.views.decorators.csrf import csrf_exempt

LASTFM_TOKEN = "14e1db88026c7814d4ed01afac4f1e6b"
AUD_TOKEN = "52d936452cec3fa3b2127034a38febc6" # Expire 24 March
GENIUS_TOKEN = "8DnZUqI2sO53dmGaKQ-QdB7efIsIG10xKZGCOEqbDuuveLyRgYayIzblR5aUlQL0"

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

                data = {
                    'api_token': AUD_TOKEN,
                    'return': 'apple_music,spotify',
                }

                files = {
                    'file': audio,
                }

                # result = requests.post('https://api.audd.io/', data=data, files=files)
                # print(result.text)

                status = "Success"

        return render(request, "identifyTrack.html", {"audio_info":audio_info, "status": status})
    
    return render(request, "identifyTrack.html")

@csrf_exempt
def identifyTrackUploadJSON(request):

    status = "Error"
    audio_info = "None"    

    context = {
        audio_info : audio_info,
        status: status,
    }

    return HttpResponse(json.dumps(context), content_type="application/json")


def getTopTrackRegion(request):
    country_id = "spain"
    response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country={country_id}&api_key={LASTFM_TOKEN}&format=json")

    json_data = json.loads(response.text)

    return render(request, 'topTracks.html', {'result': json_data})

def getTopTrackRegionJSON(request):
    country_id = "spain"
    response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country={country_id}&api_key={LASTFM_TOKEN}&format=json")
    data = json.loads(response.text)

    return HttpResponse(json.dumps(data), content_type="application/json")
    
    
def getTrackDetailsJSON(request, name):
    genius_request = "https://api.genius.com/search?q=" + name
    genius = requests.get(genius_request, headers={'Authorization': 'Bearer ' + GENIUS_TOKEN})
    data = json.loads(genius.text)

    return HttpResponse(json.dumps(data), content_type="application/json")

def randomSongJSON(request):
    song_id = random.randint(1,10000000)
    genius_data = "None"
    chosen_song_lastFM = "None"
    lastFM_data_detailed = "None"


    genius_request = "https://api.genius.com/songs/" + str(song_id)
    genius = requests.get(genius_request, headers={'Authorization': 'Bearer ' + GENIUS_TOKEN})
    genius_data = json.loads(genius.text)

    if genius_data['meta']['status'] == 404:
        error = {"Server Error" : "Unfortunately you weren't lucky with the roll. Please try again."}
        return HttpResponse(json.dumps(error), content_type="application/json")
    
    song_title = genius_data["response"]["song"]["title"]

    lastFM = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=track.search&track={song_title}&api_key={LASTFM_TOKEN}&format=json")
    lastFM_data = json.loads(lastFM.text)

    if len(lastFM_data['results']['trackmatches']['track']) > 0:
        chosen_song_lastFM = lastFM_data['results']['trackmatches']['track'][0]

        LFM_song_title = chosen_song_lastFM['name']
        LFM_song_artist = chosen_song_lastFM['artist']

        lastFM_detailed_song = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={LASTFM_TOKEN}&artist={LFM_song_artist}&track={LFM_song_title}&format=json")
        lastFM_data_detailed = json.loads(lastFM_detailed_song.text)

    data = {
        "genius_data" : genius_data,
        "lastFM_data": chosen_song_lastFM,
        "lastFM_data_detailed": lastFM_data_detailed,
    }

    return HttpResponse(json.dumps(data), content_type="application/json")