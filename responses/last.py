# -*- coding: utf-8 -*
import requests

from data import DataAccess
from .AbstractResponse import *
from dota2py import api
from dota2py import data
import random


class ResponseLast(AbstractResponse):

    match_performance_template = "As {hero} you went {k}:{d}:{a} with {GPM} GPM finishing at level {level}"

    RESPONSE_KEY = "#last"

    HELP_RESPONSE = "Shows your personel stats from the last game, add a user argument to find someone elses stats"

    DOTABUFF_LINK_TEMPLATE = "http://www.dotabuff.com/matches/{id}"

    SASS_PERCENTAGE = 0.005

    def __init__(self, msg):
        super(ResponseLast, self).__init__(msg)

    def _respond(self):

        if random.random() < ResponseLast.SASS_PERCENTAGE:
            print("#last - sassy override")
            return "Bitch, you can't last for shit"


        print("Setting Key & Account ID")
        secrets = DataAccess.get_secrets()
        api.set_api_key(secrets["DOTA_KEY"])

        user = DataAccess.DataAccess().get_user("GROUPME_ID", self.msg.get_sender_uid())
        account_id = user['STEAM_ID']

        print("Got Account ID")
        # Get a list of recent matches for the player
        matches = api.get_match_history(account_id=account_id)["result"]["matches"]

        #Get the full details for a match
        # match = api.get_match_details(matches[0]["match_id"])
        URL = r"https://api.steampowered.com/IDOTA2Match_570/GetMatchHistoryBySequenceNum/v1"

        params = {
            "key": secrets["DOTA_KEY"],
            "start_at_match_seq_num": matches[0]['match_seq_num'],
            "matches_requested": 1
        }

        response = requests.get(URL, params=params)
        match = json.loads(response.content)['result']['matches'][0]
        match_id = matches[0]["match_id"]

        dotabuff_link = ResponseLast.DOTABUFF_LINK_TEMPLATE.format(id=match_id)

        print("Got Match Details")
        player_num = 0

        for x in match["players"]:
            if x["account_id"] == user['DOTA_ID']:
                out = ""
                print("Got self.sender Data")

                #Stats?
                print(player_num)
                msg = ResponseLast.match_performance_template.format(hero=data.get_hero_name(x["hero_id"])["localized_name"],
                                                            k=str(x["kills"]),
                                                            d=str(x["deaths"]),
                                                            a=str(x["assists"]),
                                                            GPM=str(x["gold_per_min"]),
                                                            level=str(x["level"])
                                                            )
                out += msg + "\n"

                #Items?
                finalItems = "Your items: "
                for itemNum in range(0, 6):
                    if x["item_" + str(itemNum)] != 0 and x["item_" + str(itemNum)] is not None:
                        try:
                            finalItems += str(data.get_item_name(x["item_" + str(itemNum)])["name"]) + ", "
                        except:
                            finalItems += "unknown item ({}), ".format(x["item_" + str(itemNum)])
                out += finalItems + "\n"

                backpackItems = "Backpack: "
                for itemNum in range(0, 3):
                    if x["backpack_" + str(itemNum)] != 0 and x["backpack_" + str(itemNum)] is not None:
                        try:
                            backpackItems += str(data.get_item_name(x["backpack_" + str(itemNum)])["name"]) + ", "
                        except:
                            backpackItems += "unknown item ({}), ".format(x["backpack_" + str(itemNum)])
                out += backpackItems + "\n"

                neutralItem = "Neutral Item: "
                if x["item_neutral"] != 0 and x["item_neutral"] is not None:
                    try:
                        neutralItem += str(data.get_item_name(x["item_neutral"])["name"]) + ", "
                    except:
                        neutralItem += "unknown item ({}), ".format(x["item_neutral"])
                out += neutralItem + "\n"

                emojis = {
                    0: '❌',
                    1: '✅'
                }

                buffs = "Aghs {0} | Shard {1} | Moonshard {2}".format(
                    emojis[x["aghanims_scepter"]],
                    emojis[x["aghanims_shard"]],
                    emojis[x["moonshard"]],
                )

                out += buffs + "\n"

                #Win?
                #@todo fix this to incorporate woody's bugfix
                if player_num < 5 and match["radiant_win"]:
                    out += "You Won! "
                elif player_num > 4 and not match["radiant_win"]:
                    out += "You Won! "
                else:
                    out += "You Lost.... Bitch "
                out += str(match_id) + " " + dotabuff_link
                return out
            player_num = player_num + 1
