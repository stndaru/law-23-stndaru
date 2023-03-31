import json, requests, mutagen, random, time

# Sync this with Views.py
LASTFM_TOKEN = "14e1db88026c7814d4ed01afac4f1e6b"
AUD_TOKEN = "52d936452cec3fa3b2127034a38febc6" # Expire 24 March 2023, Max 300 Requests
GENIUS_TOKEN = "8DnZUqI2sO53dmGaKQ-QdB7efIsIG10xKZGCOEqbDuuveLyRgYayIzblR5aUlQL0"

def randomSongJSONFunction():
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
        return json.dumps(context)

    return json.dumps(data)