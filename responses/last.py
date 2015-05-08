# -*- coding: utf-8 -*
from AbstractResponse import *
from dota2py import api
from dota2py import data
import random
import pprint

class ResponseLast(AbstractResponse):

    match_performance_template = "As {hero} you went {k}:{d}:{a} with {GPM} GPM finishing at level {level}"

    RESPONSE_KEY = "#last"

    HELP_RESPONSE = "Shows your personel stats from the last game, add a user argument to find someone elses stats"

    DOTABUFF_LINK_TEMPLATE = "http://www.dotabuff.com/matches/{id}"

    SASS_PERCENTAGE = 0.005

    def __init__(self, msg, sender):
        super(ResponseLast, self).__init__(msg, sender)

    def respond(self):

        if random.random() < ResponseLast.SASS_PERCENTAGE:
            print("#last - sassy override")
            return "Bitch, you can't last for shit"

        print "Starting"

        if not AbstractResponse.has_steamID(self.sender):
            return "I don't know your SteamID! Set it with '#set ID'"

        if not AbstractResponse.has_dotaID(self.sender):
            return "I don't know your DOTA ID! Set it with '#setDota ID'"

        print "Setting Key & Account ID"
        api.set_api_key(AbstractResponse.key)

        account_id = AbstractResponse.name_to_steamID(self.sender)

        print "Got Account ID"
        # Get a list of recent matches for the player
        matches = api.get_match_history(account_id=account_id)["result"]["matches"]

        #Get the full details for a match
        match = api.get_match_details(matches[0]["match_id"])

        match_id = match['result']['match_id']

        dotabuff_link = ResponseLast.DOTABUFF_LINK_TEMPLATE.format(id=match_id)

        print "Got Match Details"
        player_num = 0

        for x in match["result"]["players"]:
            if int(x["account_id"]) == AbstractResponse.name_to_dotaID(self.sender):
                out = ""
                print "Got self.sender Data"

                #Stats?
                print player_num
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
                            finalItems += "unknown item, "

                out += finalItems + "\n"

                #Win?
                #@todo fix this to incorporate woody's bugfix
                if player_num < 5 and match["result"]["radiant_win"]:
                    out += "You Won! "
                elif player_num > 4 and not match["result"]["radiant_win"]:
                    out += "You Won! "
                else:
                    out += "You Lost.... Bitch "
                out += str(match_id) + " " + dotabuff_link
                return out
            player_num = player_num + 1
