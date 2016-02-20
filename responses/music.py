# -*- coding: utf-8 -*-
from AbstractResponse import AbstractResponse
import requests
import os
import json
import sys
import pprint
import time

class ResponseMusic(AbstractResponse):
    RESPONSE_KEY = "#music"

    def __init__(self, msg):
        super(ResponseMusic, self).__init__(msg)

    def respond(self):
        out = ""
        print("lastfm")
        lastfm_endpoint = "http://ws.audioscrobbler.com/2.0/"
        person_status_template = u"{name} : {song}\n"
        MAX_TIME_DIFFERENCE = 60 * 60 # an hour in seconds
        key = None
        try:
            with open('local_variables.json') as f:
                local_var = json.load(f)
                key = local_var["LASTFM_KEY"]
        except EnvironmentError:
                key = os.getenv("LASTFM_KEY")

        if not key:
            print("failed to load LASTFM_KEY--- aborting!")
            return

        req_data = dict()
        req_data['format'] = 'json'
        req_data['limit'] = 1
        req_data['method'] = "user.getRecentTracks"

        time_now = time.time()

        for person, username in AbstractResponse.GroupMetoLastfm.iteritems():
            try:
                if not username:
                    continue
                print("Looking up username: " + username)
                req_data['user'] = username
                req_data['api_key'] = key

                response = requests.post(lastfm_endpoint, data=req_data)
                response = response.json()

                if not response:
                    continue

                last_track = response['recenttracks']['track'][0]
                t_diff = time_now - int(last_track['date']['uts'])

                if t_diff > MAX_TIME_DIFFERENCE:
                    print("\t song out of date ({0:.0f}s)".format(t_diff))
                    continue

                on_now = '@attr' in last_track and last_track['@attr']['nowplaying'] == 'true'
                #if not on_now
                # continue

                trackname = last_track['name']
                artist = last_track['artist']['#text']
                song = u"{} by {}".format(trackname, artist)

                if on_now:
                    song = song + " (now!)"

                out += person_status_template.format(name=person, song=song)
            except Exception, e:
                line_fail = sys.exc_info()[2].tb_lineno
                print("\tError: {} on line {}".format(repr(e), line_fail))

        return out
