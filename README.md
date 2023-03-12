# Audio Central v1
#### Layanan Aplikasi & Web Project by Stefanus Ndaru W - 2006526812

## App Explanation
### Overview
Audio central is a web service oriented around audio, but mainly music. Here you can do multiple actions regarding music searching that are based mainly on two popular music information platform: Last.FM and Genius. Currently, you can 
1. Recognize a song based on uploaded audio file
2. Select a random song
3. Search top tracks based on region 
4. Search a song by title

### Background
This project was originated by my passion for music listening, and not through the idea from the assignment's details because I just realized it was mentioned there in the last day. Originally, I wanted to do a fully centralized audio including Text-Transcription using OpenAI Whisper, but sadly it was too costly to run GPU, a necessary component, in GCP (it costs up to $3000/month). So I set back that idea and decide to make a song recognizer that could integrate result with Genius and Last.FM, 2 big platform for looking up song details

---
## List of Functions


### [Flagship Feature] Song Recognizer
Recognize a song based on an audio uploaded with constraints of maximum 2MB size and 20 second duration, and fetched the song's details from Genius and Last.FM, if they exist   

**Parameter List**
```
mp3 file of target song with max duration of 20 second and max size of 2MB
```
**Curl Call Example**
```
curl http://127.0.0.1:8000/identify-track/json -i -F csrfmiddlewaretoken=<csrf-token> -F audio=@<path/to/file>;type=audio/mpeg
```
**Result Example**

>genius_data = data result from Genius platform   
>genius_data_detailed = data result from Genius track specific detail     
>lastFM_data = data result from Last.FM search    
>lastFM_data_detailed = data result from Last.FM track specific detail   

You might receive errors when uploading, which can be viewed on the corresponding error message through `status_description`.    

For further details, you can view the API guide for Genius (https://docs.genius.com/) and Last.FM (https://www.last.fm/api)


```json
{
    "status" : "<request_status>",
    "audio_info" : "<track_length>",
    "status_description" : "<status_description>",
    "song_title" : "<song_title>",
    "artist" : "<artist_name>",
    "analyze_result" : {"..."},
    "genius_data" : {"..."},
    "genius_data_detailed" : {"..."},
    "lastFM_data" : {"..."},
    "lastFM_data_detailed" : {"..."},
}

```
**Web View URL**
```
<link>/identify-track
```
**Screenshot Example**    
Web View    
![Identifier-Web-View](./media/identifier-1.png)
JSON View 
![Identifier-JSON-View](./media/identifier-2.png)   

### [Flagship Feature] Song Randomizer
Select a random song that exist in Genius's library and returns the detailing data of the song from Genius and Last.FM (if exist)    

**Parameter List**
```
none
```
**Curl Call Example**
```
curl http://127.0.0.1:8000/random/json
```
**JSON Result**

>genius_data = data result from Genius platform    
>lastFM_data = data result from Last.FM search    
>lastFM_data_detailed = data result from Last.FM track specific detail

```json
{
    "genius_data" : {
        "meta": {"..."},
        "response": {"..."}
    },
    "lastFM_data" : {
        "name" : "<song_name>",
        "artist" : "<artist_name>",
        "url" : "<song_lastfm_url>",
        "streamable" : "<song_streamable>",
        "listeners" : "<song_listeners>",
        "image" : {"..."},
        "mbid" : "<song_mbid>",
    },
    "lastFM_data_detailed" : {
        "track" : {
            "name" : "<song_name>",
            "url" : "<song_lastfm_url>",
            "duration" : "<song_duration>",
            "streamable" : {"..."},
            "listeners" : "<song_listeners>",
            "playcount" : "<song_playcount>",
            "artist" : {"..."},
            "toptags" : {"..."},       
        }
    }
}

```
**Web View URL**
```
<link>/random/json
```
Occasionally, this feature call will result in a `error` result which was caused by the random nature of the randomizer and the inconsistency of Genius library. Solving this can be done by retrying the call again.

**Screenshot Example**    
JSON View 
![Identifier-JSON-View](./media/random-s1.png) 


### Top Tracks by Region
Find top tracks that are currently being played based on country with data obtained from Last.FM   

**Parameter List**
```
ISO 3166 country code
```
**Curl Call Example**
```
http://127.0.0.1:8000/top-tracks-region/<region>
```
**Result Example**
```json
{
    "country": "country",
    "track": {
        "0" : {
            "name" : "<song_name>",
            "duration": "<song_duration>",
            "listeners" : "<song_listeners>",
            "mbid" : "<song_mbid>",
            "url" : "<song_lastfm_url>",
            "streamable" : {"..."},
            "artist" : {"..."},
            "image" : {"..."},
            "@attr" : "<song_attribute>",
        },
        "1" : {
            "..."
        }, "..."
    }
}
```
**Web View URL**
```
<link>/top-tracks-region/<country>
```
**Screenshot Example**    
Web View 
![Identifier-JSON-View](./media/toptrack-s1.png) 
JSON View     
![Identifier-JSON-View](./media/toptrack-s2.png) 

### Search Song based on Name
Search a song based on name and fetch result from Genius library, and fetch several songs with similar title to the inputted name    

**Parameter List**
```
valid song name
```
**Curl Call Example**
```
http://127.0.0.1:8000/search-name/json/<song-name>
```
**Result Example**
```json
{
    "meta": {
        "status" : "<service-call-status-response>",
    },
    "response" : {
        "hits" : {
            "0": {"..."},
            "1": {"..."},
            "..."
        }
    }
}
```
**Web View URL**
```
<link>/search-name/json/<song-name>
```
**Screenshot Example**    
JSON View 
![Identifier-JSON-View](./media/search-s1.png) 

## Application/Web Service Development Difficulties & Complexity
Eventhough the web service seems simple, there are a lot of difficulties that I had to face:    
1. File Upload via Form and Curl    
asda
2. API Management (Fetching & Error Handling)    
Lorem
3. API Merging & Requests   
Lorem
4. Hardware Limitation   
Lorem
5. Front-End and Back-End    
Lorem

## Application/Web Service Usability/Urgency
This website can have multiple functionalities based on the available features, which are:   
1. Find an unknown song title and details from an audio
2. Search for song you want to find the details of
3. Find song details in general via JSON response easily
4. Search for a random song
5. Search for top tracks in a country

## Application/Web Service Uniqueness
Although there are a few song recognizer software, only few could support a simple yet effective function and webservice that could integrate multiple platforms. Currently, there are no song recognizer platform that could automatically fetch result from Genius and Last.FM, and if you're an avid Last.FM user, this web service is for you. Just upload a small clip of a song, and this service will fetch the corresponding Genius and Last.FM details for your convenience! No longer are the days you have to manually find the song after obtaining the title. And best of all, this is the only platform where you can integrate it anywhere that supports file upload and JSON result!  
     
On top of this, you can also access several other features such as song randomizer that also fetches data from Genius and Last.FM. Now if you want something fresh, just hit up the randomizer and start listening to new songs for you!


---

# How to run
Credit to Adrian Ardizza (Meta501)
### Locally
#### Requirements
- Python 3.10
- pipenv (install using python -m pip install pipenv)
#### Installation
- Run `pipenv install` on the project directory
- Create a new `.env` file based on `.env.example`
- Run `pipenv shell`
- Run `python manage.py runserver`
### Docker (For deployment on GCP)
#### Requirements
- Latest version of Docker
#### Installation
- Run `docker-compose up` on the project directory
- Application will deploy all necessary dependencies automatically
- If an error occurs during migration, rerun `docker-compose up`
