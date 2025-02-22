#Project name: DJ-Running
#Authors: Jorge García de Quirós, Sandra Baldassarri, Pedro Álvarez
#Affiliation/Institution: Computer Science and Systems Engineering Department, University of Zaragoza (Spain)
#Paper: RIADA: a machine-learning based infrastructure for recognising the emotions of the Spotify songs
#Date: October, 2020

import pprint
import pickle as pickle
import simplejson as json
import math


f = open('tracks.pkl', 'rb')
data = pickle.load(f)


print('tracks', data['ntracks'], 'offset', data['offset'], 'playlists', data['playlists'])

tracks = data['tracks']
total = float(data['playlists'])

top = [ (obj, id) for id, obj in list(tracks.items())]

top.sort(key=lambda o : o[0]['count'])
top.reverse()

for obj, id in top[:200]:
    frac = 100.0 * obj['count'] / total
    print("%s %d %.2f %s %s" % (id, obj['count'], frac, obj['title'], obj['artist']))


out = {}
min_count = 5
for obj, id in top:
    if id and obj['count'] >= min_count:
        idf = math.log10(total / obj['count'])
        ppm = 1000.0 * obj['count'] / total
        #out[id] = ppm;
        out[id] = idf;

#out['backoff_probability'] = 1000.0 * 1. / total
#out['backoff_idf'] = math.log10(total * 2 / 1)

f = open('results.js', 'w')
f.write(json.dumps(out))
f.close()


