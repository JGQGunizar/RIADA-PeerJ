#!/usr/bin/python
# coding: utf-8

#Project name: DJ-Running
#Authors: Jorge García de Quirós, Sandra Baldassarri, Pedro Álvarez
#Affiliation/Institution: Computer Science and Systems Engineering Department, University of Zaragoza (Spain)
#Paper: RIADA: a machine-learning based infrastructure for recognising the emotions of the Spotify songs
#Date: October, 2020

import sys
import os
import json
from pymongo import MongoClient
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint

client_id = "client_id"
client_secret = "client_secret"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def extract_spotify_id_by_params(title, artist, album):
    results = sp.search(q='track:"' + title + '"artist:"' + artist + '"album:"' + album + '"', type='track', limit=1)
    if len(results['tracks']['items'])>0 :
    	return results['tracks']['items'][0]['id']
    else:
    	return -1

def extract_audio_features_by_id(id):
    features = sp.audio_features(id)
    return features

def extract_audio_analysis_by_id(id):
    analysis = sp.audio_analysis(id)
    return analysis

#WIP
def create_object(title,album,artist,analysis,features,id,data,mbid):
	musicInfo = {
	    'name' : title,
	    'album' : album,
	    'artist' : artist    
	}

	spotifyFeat = {
	    'audioSections' : analysis['sections'],
	    'danceability' : features[0]['danceability'],
	    'energy' : features[0]['energy'],
	    'key' : features[0]['key'],
	    'loudness': features[0]['loudness'],
	    'mode' : features[0]['mode'],
	    'speechiness' : features[0]['speechiness'],
	    'acousticness' : features[0]['acousticness'],
	    'instrumentalness' : features[0]['instrumentalness'],
	    'liveness' : features[0]['liveness'],
	    'valence' : features[0]['valence'],
	    'tempo' : features[0]['tempo'],
	    'duration_ms' : features[0]['duration_ms']
	}

	acousticBrainzFeat = {
	    'danceability' : data["highlevel"]["danceability"],
	    'gender' : data["highlevel"]["danceability"],
	    'genre_dortmund' : data["highlevel"]["genre_dortmund"],
	    'genre_electronic' : data["highlevel"]["genre_electronic"],
	    'genre_rosamerica' : data["highlevel"]["genre_rosamerica"],
	    'genre_tzanetakis' : data["highlevel"]["genre_tzanetakis"],
	    'ismir04_rhythms' : data["highlevel"]["ismir04_rhythm"],
	    'mood_acoustic' : data["highlevel"]["mood_acoustic"],
	    'mood_aggressive' : data["highlevel"]["mood_aggressive"],
	    'mood_electronic' : data["highlevel"]["mood_electronic"],
	    'mood_happy' : data["highlevel"]["mood_happy"],
	    'mood_party' : data["highlevel"]["mood_party"],
	    'mood_relaxed' : data["highlevel"]["mood_relaxed"],
	    'mood_sad' : data["highlevel"]["mood_sad"],
	    'moods_mirex' : data["highlevel"]["moods_mirex"],
	    'timbre' : data["highlevel"]["timbre"],
	    'tonal_atonal' : data["highlevel"]["tonal_atonal"],
	    'voice_instrumental' : data["highlevel"]["voice_instrumental"],
	}

	feat= {
	    'spotifyFeat' : spotifyFeat,
	    'acousticBrainzFeat' : acousticBrainzFeat,
	    'availableFeatures' : ['SPOTIFY', 'ACOUSTICBRAINZ']
	}

	music_object = {
	    '_id' : id,
	    'mbid' : mbid,
	    'musicInfo' : musicInfo,
	    'features' : feat
	}

	return music_object


def readSongs(directory):
	print (directory)
	for filename in os.listdir(directory):
		if filename.endswith(".json"): 
			#read_file
			with open(directory+"/"+filename) as f:
				data = json.load(f)
			if ("metadata" in data.keys() and "tags" in data["metadata"].keys() and "album" in data["metadata"]["tags"].keys() 
			and "artist" in data["metadata"]["tags"].keys() and "title" in data["metadata"]["tags"].keys()):
				album =  data["metadata"]["tags"]["album"][0]
				artist = data["metadata"]["tags"]["artist"][0]
				title = data["metadata"]["tags"]["title"][0]

				#search in sp
				try:
					id = extract_spotify_id_by_params(title,artist,album)

					if id != -1:
						features = extract_audio_features_by_id(id)

						analysis = extract_audio_analysis_by_id(id)

						#if not in db insert
						if (collection.find({"_id" : id})).count()<1:
							#Creating a new object
							m_object = create_object(title,album,artist,analysis,features,id,data,filename[:-7])
							#insert
							collection.insert(m_object)
				except Exception:
					print(str("Error: " + filename[:-7]))

		#is directory
		else:
			readSongs(directory+"/"+filename)


#Cliente mongo a la bd
client = MongoClient('mongodb://localhost:27017/')
#Asocia database
db = client.mrs_db
#Asocia collection
collection = db.djrunning


if len(sys.argv) != 2:
	print ("1 argument required")
else:
	directory = sys.argv[1]
	readSongs(directory)

