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

        #Get Xbox Second
        for person, xboxid in AbstractResponse.GroupMetoXbox.iteritems():

            xbox_url = "https://xboxapi.com/v2/{id}/presence"

            key = "0"
            print(person)
            try:
                with open('local_variables.json') as f:
                    local_var = json.load(f)
                    key = local_var["XBOX_KEY"]
            except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
                key = os.getenv('XBOX_KEY')
            except:
                print "Something went very wrong in #now for the Xbox key"

            response = requests.get(xbox_url.format(id=xboxid), headers={'X-AUTH': key})
            if response.json()["state"] == "Online":
                print("is Online!")
                game = response.json()["devices"][0]["titles"][0]["name"]
                out += ResponseNow.person_status_template.format(name=person, status=game, system="Xbox")

        if not out:
            return "Nobody's online :("
        return out


