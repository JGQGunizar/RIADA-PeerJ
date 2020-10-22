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
def create_object(analysis,features,id,score,label_s,label_h,label_a,label_r):
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

	feat= {
	    'spotifyFeat' : spotifyFeat,
	    'availableFeatures' : ['SPOTIFY']
	}

	music_object = {
	    '_id' : id,
	    'ranking': score,
	    'features' : feat,
	    'happy' : label_h,
	    'sad': label_s,
	    'angry': label_a,
	    'relaxed': label_r

	}

	return music_object


def readSongs(songs, data):
	for element in songs:
		#search in sp
		id = element

		if id != -1 and data[element]<=2.50:
						#if not in db insert
			if (collection.find({"_id" : id})).count()<1:

				features = extract_audio_features_by_id(id)

				analysis = extract_audio_analysis_by_id(id)

				#Creating a new object
				if (sys.argv[2]=="happy"):
					m_object = create_object(analysis,features,id,data[id],0,1,0,0)
				elif(sys.argv[2] == "sad"):
					m_object = create_object(analysis,features,id,data[id],1,0,0,0)
				elif(sys.argv[2] == "angry"):
					m_object = create_object(analysis,features,id,data[id],0,0,1,0)
				elif(sys.argv[2] == "relaxed"):
					m_object = create_object(analysis,features,id,data[id],0,0,0,1)
				#insert
				collection.insert(m_object)

			else :
				collection.update_one({"_id": id},{"$set":{sys.argv[2]:1}})


#Cliente mongo a la bd
client = MongoClient('mongodb://localhost:27017/')
#Asocia database
db = client.mrs_db
#Asocia collection
collection = db.djrunning_big_SPv2


if len(sys.argv) != 3:
	print ("2 arguments required")
else:
	file = sys.argv[1]
	with open(file) as f:
		data = json.load(f)
	ids_list = [x for x in data]
	readSongs(ids_list, data)

