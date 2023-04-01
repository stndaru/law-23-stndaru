from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from .models import Document, TranscriptResult, TemporaryAudio
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from .acfunctions.FetchTrack import *
from .acfunctions.RandomSong import *
from .acfunctions.TranscribeText import *
import json, requests, mutagen, random, time, pika

LASTFM_TOKEN = "14e1db88026c7814d4ed01afac4f1e6b"
AUD_TOKEN = "52d936452cec3fa3b2127034a38febc6" # Expire 24 March 2023, Max 300 Requests
GENIUS_TOKEN = "8DnZUqI2sO53dmGaKQ-QdB7efIsIG10xKZGCOEqbDuuveLyRgYayIzblR5aUlQL0"

# Main Landing Page
def main(request):
    return render(request, 'index.html')


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
    result = randomSongJSONFunction()
    return HttpResponse(result, content_type="application/json")

def transcribeText(request):
    status = "Error"
    audio_info = "None"
    status_description = "Unknown error, please try again"
    transcribe_result = "None"

    if request.method=="POST":
    
        # try:
        if request.FILES["audio"]:
            audio = request.FILES["audio"]

            audio_info = mutagen.File(audio).info
            transcribed_audio_obj = TranscriptResult.objects.create(status="In Progress")
            storage_obj = TemporaryAudio.objects.create(audio = audio)

            rmq_data = {
                "task" : "transcribe",
                "audio_info" : audio_info.length,
                "obj_id" : transcribed_audio_obj.id,
                "storage_id" : storage_obj.id
            }

            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()

            channel.queue_declare(queue='transcribe0')

            channel.basic_publish(exchange='', routing_key='transcribe0', body=json.dumps(rmq_data))
            print(" [x] Sent call")
            connection.close()

            # context = transcribeTextData(audio, audio_info, transcribed_audio_obj, None, None)
            context = {
                "status" : "In Progress",
                "status_description" : "Transcription is in progress...",
                "id" : transcribed_audio_obj.id
            }

            return render(request, "transcribeText.html", context)

        # except Exception as e:
        #     status_description = f"We've discovered an error while processing your file. Make sure you've uploaded a correct non-corrupt file:\n {e}"


        context = {
            "status" : status,
            "audio_info" : audio_info.length,
            "status_description" : status_description,
        }

        return render(request, "transcribeText.html", context)
    
    return render(request, "transcribeText.html")

def transcribeTextView(request,id):
    data = get_object_or_404(TranscriptResult, pk=id)
    if data.status == "In Progress":
        context = {
            "id" : data.id,
            "status":"In Progress",
            "status_description" : "Text is still being transcribed",
        }
    else:
        context = {
            "id" : data.id,
            "status":"Success",
            "audio_info" : str(data.audio_info),
            "status_description" : "Successfully transcribed",
            "transcribe_result" : data.transcribe_result,
            "sentiment_result" : data.sentiment_result,
        }
        
    return HttpResponse(json.dumps(context), content_type="application/json")
