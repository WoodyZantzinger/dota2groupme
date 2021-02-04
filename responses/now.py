# -*- coding: utf-8 -*
from data import DataAccess
from .AbstractResponse import AbstractResponse
import requests
import steamapi
import os
import json


class ResponseNow(AbstractResponse):


    #api = steamapi.core.APIConnection(AbstractResponse.local_var["DOTA_KEY"])

    person_status_template = "{name} : {status} on {system}\n"

    RESPONSE_KEY = "#now"

    def __init__(self, msg):
        super(ResponseNow, self).__init__(msg)

    def _respond(self):
        secrets = DataAccess.get_secrets()
        api = steamapi.core.APIConnection(secrets["DOTA_KEY"])

        out = ""

        #Get Steam First
        for person, steamid in AbstractResponse.GroupMetoSteam.items():
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
            print("Something went very wrong in #now for the Xbox key")
        #Get Xbox Second
        for person, xboxid in AbstractResponse.GroupMetoXbox.items():
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

        if not out:
            return "Nobody's online :("
        return out


