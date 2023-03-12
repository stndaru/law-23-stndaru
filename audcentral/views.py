from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from .models import Document
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
import json, requests, mutagen, random, time

LASTFM_TOKEN = "14e1db88026c7814d4ed01afac4f1e6b"
AUD_TOKEN = "52d936452cec3fa3b2127034a38febc6" # Expire 24 March 2023, Max 300 Requests
GENIUS_TOKEN = "8DnZUqI2sO53dmGaKQ-QdB7efIsIG10xKZGCOEqbDuuveLyRgYayIzblR5aUlQL0"

# Main Landing Page
def main(request):
    return render(request, 'index.html')

# Supporting Function
def fetchTrack(audio, audio_info):
    status = "Error"
    status_description = "Unknown error, please try again"
    analyze_result = "None"
    genius_data = "None"
    genius_data_detailed = "None"
    lastFM_data = "None"
    lastFM_data_detailed = "None"

    data = {
        'api_token': AUD_TOKEN,
        'return': 'apple_music,spotify',
        }

    files = {
        'file': audio,
    }

    result = requests.post('https://api.audd.io/', data=data, files=files)
    analyze_result = json.loads(result.text)

    if analyze_result['status'] == "error":
        status_description = "Our service could not identify the song. Please make sure to upload the correct file or an identifiable song and try again. \nDetailed error: "
        status_description += f"{analyze_result['error']['error_code']} | {analyze_result['error']['error_message']}"

        context = {
                    "status" : status,
                    "audio_info" : audio_info,
                    "status_description" : status_description,
                    "song_title" : analyze_result,
                    "artist" : analyze_result,
                    "analyze_result" : analyze_result,
                    "genius_data" : genius_data,
                    "genius_data_detailed" : genius_data_detailed,
                    "lastFM_data" : lastFM_data,
                    "lastFM_data_detailed" : lastFM_data_detailed,
                }
        return context
        
    else:
        try:
            song_title = analyze_result['result']['title']
            if analyze_result['result'] is None or len(analyze_result['result']) == 0 or analyze_result['result']['title']:
                status_description = "We've received your audio, but unfortunatly, our service could not identify the song."

        except:
            status_description = "Our service could not identify the song. Please make sure to upload the correct file or an identifiable song and try again."
            context = {
                "status" : status,
                "audio_info" : audio_info,
                "status_description" : status_description,
                "song_title" : analyze_result,
                "artist" : analyze_result,
                "analyze_result" : analyze_result,
                "genius_data" : genius_data,
                "genius_data_detailed" : genius_data_detailed,
                "lastFM_data" : lastFM_data,
                "lastFM_data_detailed" : lastFM_data_detailed,
            }
            return context

        # Check Genius
        genius_request = "https://api.genius.com/search?q=" + song_title
        genius = requests.get(genius_request, headers={'Authorization': 'Bearer ' + GENIUS_TOKEN})
        genius_data = json.loads(genius.text)

        if len(genius_data['response']['hits']) > 0:
            genius_song_api_call = genius_data['response']['hits'][0]['result']['api_path']

            genius_request_detailed = "https://api.genius.com" + genius_song_api_call
            genius_detailed = requests.get(genius_request_detailed, headers={'Authorization': 'Bearer ' + GENIUS_TOKEN})
            genius_data_detailed = json.loads(genius_detailed.text)

        # Check LASTFM
        lastFM = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=track.search&track={song_title}&api_key={LASTFM_TOKEN}&format=json")
        lastFM_data = json.loads(lastFM.text)

        if len(lastFM_data['results']['trackmatches']['track']) > 0:
            chosen_song_lastFM = lastFM_data['results']['trackmatches']['track'][0]

            LFM_song_title = chosen_song_lastFM['name']
            LFM_song_artist = chosen_song_lastFM['artist']

            lastFM_detailed_song = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={LASTFM_TOKEN}&artist={LFM_song_artist}&track={LFM_song_title}&format=json")
            lastFM_data_detailed = json.loads(lastFM_detailed_song.text)
        
        status = "Success"
        status_description = "Successfully analyzed song and fetched the result"

    context = {
        "status" : status,
        "audio_info" : audio_info,
        "status_description" : status_description,
        "song_title" : analyze_result['result']['title'],
        "artist" : analyze_result['result']['artist'],
        "analyze_result" : analyze_result,
        "genius_data" : genius_data,
        "genius_data_detailed" : genius_data_detailed,
        "lastFM_data" : lastFM_data,
        "lastFM_data_detailed" : lastFM_data_detailed,
    }

    return context


# Identify Uploaded Track
def identifyTrackUpload(request):
    status = "Error"
    audio_info = "None"
    status_description = "Unknown error, please try again"
    analyze_result = "None"
    genius_data = "None"
    genius_data_detailed = "None"
    lastFM_data = "None"
    lastFM_data_detailed = "None"

    if request.method=="POST":
    
        try:
            if request.FILES["audio"]:
                audio = request.FILES["audio"]

                audio_info = mutagen.File(audio).info

        except:
            status_description = "We've discovered an error while processing your file. Make sure you've uploaded a correct non-corrupt file"


        if audio_info.length < 20 and audio.size < 19971520:

            context = fetchTrack(audio, audio_info)
            return render(request, "identifyTrack.html", context)

        else:
            status_description = "Please upload a song in MP3 format and with size less than 2MB AND duration less than 20 seconds" 

        context = {
            "status" : status,
            "audio_info" : audio_info,
            "status_description" : status_description,
            "analyze_result" : analyze_result,
            "genius_data" : genius_data,
            "genius_data_detailed" : genius_data_detailed,
            "lastFM_data" : lastFM_data,
            "lastFM_data_detailed" : lastFM_data_detailed,
        }

        return render(request, "identifyTrack.html", context)
    
    return render(request, "identifyTrack.html")

@csrf_exempt
def identifyTrackUploadJSON(request):

    status = "Error"
    audio_info = "None" 

    try:
        if request.method=="POST":
            if request.FILES["audio"]:

                audio = request.FILES['audio']
                audio_info = mutagen.File(audio).info.length

                # TODO Implementation Here
                if audio_info < 20 and audio.size < 19971520:
                    context = fetchTrack(audio, audio_info)
                    return HttpResponse(json.dumps(context), content_type="application/json")
                
                else:
                    status_description = "Please upload a song in MP3 format and with size less than 2MB AND duration less than 20 seconds" 

        context = {
            "status" : status,
            "audio_info" : audio_info,
            "status_description" : status_description,
        }

        return HttpResponse(json.dumps(context), content_type="application/json")
    
    except:
        return HttpResponseBadRequest("Please use POST with attached file to analyze and receive JSON result")


# Get Top Track Region
def getTopTrackRegion(request, country):
    country_id = country
    response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country={country_id}&api_key={LASTFM_TOKEN}&format=json")
    json_data = json.loads(response.text)

    try: 
        if json_data['error']:
            return render(request, 'topTracks.html', {'error': json_data})
    except:
        pass

    context = {
        "country" : country,
        "data" : json_data,
    }

    return render(request, 'topTracks.html', context)

def getTopTrackRegionJSON(request, country):
    country_id = country
    response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country={country_id}&api_key={LASTFM_TOKEN}&format=json")
    data = json.loads(response.text)

    context = {
        "country" : country,
        "data" : data,
    }

    return HttpResponse(json.dumps(context), content_type="application/json")


# Get Track Details
def getTrackDetailsJSON(request, name):
    genius_request = "https://api.genius.com/search?q=" + name
    genius = requests.get(genius_request, headers={'Authorization': 'Bearer ' + GENIUS_TOKEN})
    data = json.loads(genius.text)

    return HttpResponse(json.dumps(data), content_type="application/json")


# Song Randomizer
def randomSongJSON(request):
    song_id = random.randint(1,10000000)
    genius_data = "None"
    chosen_song_lastFM = "None"
    lastFM_data_detailed = "None"

    try:
        genius_request = "https://api.genius.com/songs/" + str(song_id)
        genius = requests.get(genius_request, headers={'Authorization': 'Bearer ' + GENIUS_TOKEN})
        genius_data = json.loads(genius.text)

        while genius_data['meta']['status'] == 404:
            song_id = random.randint(1,10000000)
            genius_request = "https://api.genius.com/songs/" + str(song_id)
            genius = requests.get(genius_request, headers={'Authorization': 'Bearer ' + GENIUS_TOKEN})
            genius_data = json.loads(genius.text)
            time.sleep(2)
        
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
            "status" : "success",
            "genius_data" : genius_data,
            "lastFM_data": chosen_song_lastFM,
            "lastFM_data_detailed": lastFM_data_detailed,
        }
    except:
        context = {
            "status" : "error",
            "message" : "Encountered error, please try again"
        }
        return HttpResponse(json.dumps(context), content_type="application/json")

    return HttpResponse(json.dumps(data), content_type="application/json")