# -*- coding: utf-8 -*
from data import DataAccess
from .AbstractResponse import AbstractResponse
import os
import json
import requests


class ResponsePUBGLast(AbstractResponse):
    RESPONSE_KEY = "#pubglast"

    def __init__(self, msg):
        super(ResponsePUBGLast, self).__init__(msg)

    def _respond(self):
        out = ""

        template = "{name} did {damage} damage for {numKills} kills (placing {killRank} in kills) to finish {result} in a {gameType}\n"

        user = DataAccess.DataAccess().get_user("GROUPME_ID", self.msg.sender_id)
        canonical_name = user['Name']
        PUBGname = user['PUBG_ID']

        key = DataAccess.get_secrets()['PUBG_KEY']

        playerUrl = "https://api.pubg.com/shards/pc-na/players?filter[playerNames]={name}"
        matchUrl = "https://api.pubg.com/shards/pc-na/matches/{matchID}"


        header = {"Authorization": "Bearer " + key, "Accept": "application/vnd.api+json"}
        playerRequest = requests.get(playerUrl.format(name = PUBGname), headers=header)

        lastMatch = playerRequest.json()["data"][0]["relationships"]["matches"]["data"][0]["id"]
        userID = playerRequest.json()["data"][0]["id"]

        matchRequest = requests.get(matchUrl.format(matchID = lastMatch), headers=header)

        for player in matchRequest.json()["included"]:
            if player["type"] == "participant":
                if player["attributes"]["stats"]["playerId"] == userID:

                    stats = player["attributes"]["stats"]

                    out = template.format(name = stats["name"],
                                          damage = int(round(stats["damageDealt"], 0)),
                                          numKills = stats["kills"],
                                          killRank = stats["killPlace"],
                                          result = stats["winPlace"],
                                          gameType = matchRequest.json()["data"]["attributes"]["mapName"])

                    print(out)

        return out


