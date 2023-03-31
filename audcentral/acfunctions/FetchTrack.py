from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
import json, requests, mutagen, random, time

LASTFM_TOKEN = "14e1db88026c7814d4ed01afac4f1e6b"
AUD_TOKEN = "52d936452cec3fa3b2127034a38febc6" # Expire 24 March 2023, Max 300 Requests
GENIUS_TOKEN = "8DnZUqI2sO53dmGaKQ-QdB7efIsIG10xKZGCOEqbDuuveLyRgYayIzblR5aUlQL0"


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