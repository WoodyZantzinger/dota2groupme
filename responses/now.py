# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
import requests
import steamapi
import os
import json

class ResponseNow(AbstractResponse):

    api = steamapi.core.APIConnection(AbstractResponse.key)

    person_status_template = "{name} : {status} on {system}\n"

    RESPONSE_KEY = "#now"

    def __init__(self, msg):
        super(ResponseNow, self).__init__(msg)

    def respond(self):
        out = ""

        #Get Steam First
        for person, steamid in AbstractResponse.GroupMetoSteam.iteritems():
            steamuser = steamapi.user.SteamUser(steamid)

            playing = steamuser.currently_playing
            print(person)
            print(playing)
            if playing:
                game = playing._cache['name'][0]
                out += ResponseNow.person_status_template.format(name=person, status=game, system="Steam")


        key = None
        try:
            with open('local_variables.json') as f:
                local_var = json.load(f)
                key = local_var["XBOX_KEY"]
        except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
            key = os.getenv('XBOX_KEY')
        except:
            print "Something went very wrong in #now for the Xbox key"
        #Get Xbox Second
        for person, xboxid in AbstractResponse.GroupMetoXbox.iteritems():
            xbox_url = "https://xboxapi.com/v2/{id}/presence"
            print(person)

            response = requests.get(xbox_url.format(id=xboxid), headers={'X-AUTH': key})
            try:
                if response.json()["state"] == "Online":
                    print("is Online!")
                    game = response.json()["devices"][0]["titles"][0]["name"]
                    out += ResponseNow.person_status_template.format(name=person, status=game, system="Xbox")
            except:
                pass

        #Get Lastfm Third

        print("lastfm")
        lastfm_endpoint = "http://ws.audioscrobbler.com/2.0/"

        for person, username in AbstractResponse.GroupMetoLastfm.iteritems():
            try:
                if not username:
                    continue

                req_data = dict()
                req_data['method'] = "user.getRecentTracks"
                req_data['user'] = username

                key = None
                try:
                    with open('local_variables.json') as f:
                        local_var = json.load(f)
                        key = local_var["LASTFM_KEY"]
                except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
                        key = os.getenv("LASTFM_KEY")

                req_data['api_key'] = key
                req_data['format'] = 'json'
                req_data['limit'] = 1

                response = requests.post(lastfm_endpoint, data=req_data)
                response = response.json()

                if not response:
                    continue

                last_track = response['recenttracks']['track'][0]

                if last_track['@attr']['nowplaying'] != 'true':
                    continue

                trackname = last_track['name']
                artist = last_track['artist']['#text']
                status = "{} by {}".format(trackname, artist)

                out += ResponseNow.person_status_template.format(name=person, status=status, system="Spotify")
            except:
                pass
        if not out:
            return "Nobody's online :("
        return out


