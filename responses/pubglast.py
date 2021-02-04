# -*- coding: utf-8 -*
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

        canonical_name = (key for key,value in AbstractResponse.GroupMeIDs.items() if value==self.msg.sender_id).next()

        PUBGname = AbstractResponse.GroupMetoPUBGName[canonical_name]

        key = None
        try:
            with open('local_variables.json') as f:
                local_var = json.load(f)
                key = local_var["PUBG_KEY"]
        except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
            key = os.getenv('PUBG_KEY')
        except:
            print("Something went very wrong in #pubglast for the PUBG key")

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


