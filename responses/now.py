# -*- coding: utf-8 -*
from data import DataAccess
from .AbstractResponse import AbstractResponse
import requests
import steamapi
import os
import json


class ResponseNow(AbstractResponse):
    # api = steamapi.core.APIConnection(AbstractResponse.local_var["DOTA_KEY"])

    person_status_template = "{name} : {status} on {system}\n"

    RESPONSE_KEY = "#now"

    def __init__(self, msg):
        super(ResponseNow, self).__init__(msg)

    def _respond(self):
        secrets = DataAccess.get_secrets()
        api = steamapi.core.APIConnection(secrets["DOTA_KEY"])

        out = ""

        name_to_steamid = DataAccess.DataAccess().get_x_to_y_map("Name", "STEAM_ID")
        # Get Steam First
        for person, steamid in name_to_steamid:
            if not steamid:
                continue
            steamuser = steamapi.user.SteamUser(steamid)

            playing = steamuser.currently_playing
            print(person)
            print(playing)
            if playing:
                game = playing._cache['name'][0]
                out += ResponseNow.person_status_template.format(name=person, status=game, system="Steam")

        key = secrets["XBOX_KEY"]

        # Get Xbox Second
        name_to_xboxid = DataAccess.DataAccess().get_x_to_y_map("Name", "XBOX_ID")

        for person, xboxid in name_to_xboxid:
            if not xboxid:
                continue
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
