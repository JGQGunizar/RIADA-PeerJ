#Project name: DJ-Running
#Authors: Jorge García de Quirós, Sandra Baldassarri, Pedro Álvarez
#Affiliation/Institution: Computer Science and Systems Engineering Department, University of Zaragoza (Spain)
#Paper: RIADA: a machine-learning based infrastructure for recognising the emotions of the Spotify songs
#Date: October, 2020

import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import pprint as pp
import pickle as pickle
import atexit
import os
import argparse

max_playlists = 100000
scope = 'user-library-read'
client_id = "client_id"
client_secret = "client_secret"


def is_good_playlist(items):
    artists = set()
    albums = set()
    for item in items:
        track = item['track']
        if track:
            artists.add( track['artists'][0]['id'])
            albums.add(track['album']['id'])
    return len(artists) > 1 and len(albums) > 1

def process_playlist(which, total, playlist):
    tracks = data['tracks']

    print(which, total, data['ntracks'], len(tracks), playlist['name'])

    pid = playlist['id']
    uid = playlist['owner']['id']
    data['playlists'] += 1

    try:
        results = sp.user_playlist_tracks(uid, playlist['id'])
        # fields="items.track(!album)")

        if results and 'items' in results and is_good_playlist(results['items']):
            for item in results['items']:
                track = item['track']
                if track:
                    tid = track['id']
                    if tid not in tracks:
                        title = track['name'] 
                        artist = track['artists'][0]['name']
                        tracks[tid] = {
                            'title' : title,
                            'artist' : artist,
                            'count' : 0,
                        }
                    tracks[tid]['count'] += 1
                    data['ntracks'] += 1
        else:
            print('mono playlist skipped')
    except spotipy.SpotifyException:
        print('trouble, skipping')

def save():
    out = open('tracks.pkl', 'wb')
    pickle.dump(data, out, -1)
    out.close()

def load(c):
    if c and os.path.exists('tracks.pkl') and os.stat('tracks.pkl').st_size != 0:
        infile = open('tracks.pkl', 'rb')
        data = pickle.load(infile)
    else:
        data = {
            'playlists': 0,
            'ntracks': 0,
            'offset': -1,
            'tracks': {}
        }
    return data
    
def crawl_playlists(keywords):
	#Operators: NOT, OR
	#keywords format: https://developer.spotify.com/documentation/web-api/reference/search/search/#writing-a-query---guidelines
    limit = 50
    which = 0
    offset = 0 if data['offset'] < 0 else data['offset'] + limit
    results = sp.search(keywords, limit=limit, offset=offset, type='playlist')
    playlist = results['playlists']
    total = playlist['total']
    while playlist:
        data['offset'] = playlist['offset'] + playlist['limit']
        for item in playlist['items']:
            process_playlist(which, total, item)
            which += 1

        if playlist['next']:
            results = sp.next(playlist)
            playlist = results['playlists']
        else:
            playlist = None

parser = argparse.ArgumentParser(description='Extract tracks from Spotify playlists using the query')
parser.add_argument("-r", "--restore", help="Continues crawling from the last session", action="store_true")
parser.add_argument("-q", "--query", help="Spotify query to search playlists", nargs='+', metavar=('query'), required=True)
args = parser.parse_args()
print(args.restore)

query = ' '.join(args.query)
print(f'Downloading tracks info using the query [{query}]...')
try:
	client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
	atexit.register(save)
	data = load(args.restore)
	crawl_playlists(query)
except KeyboardInterrupt:
	print("\nEnd of the session.")
	print("Use [proc.py] to process the results...")
