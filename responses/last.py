# -*- coding: utf-8 -*
from AbstractResponse import *
from dota2py import api
from dota2py import data
import pprint

class ResponseLast(AbstractResponse):

    match_performance_template = "As {hero} you went {k}:{d}:{a} with {GPM} GPM finishing at level {level}"

    RESPONSE_KEY = "#last"

    HELP_RESPONSE = "Shows your personel stats from the last game, add a user argument to find someone elses stats"

    DOTABUFF_LINK_TEMPLATE = "http://www.dotabuff.com/matches/{id}"

    def __init__(self, msg, sender):
        super(ResponseLast, self).__init__(msg, sender)

    def respond(self):

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

                won = False
                if player_num < 5 and match["result"]["radiant_win"]:
                    won = True
                elif player_num > 4 and not match["result"]["radiant_win"]:
                    won = True
                else:
                    won = False
                results_are_poor = ResponseLast.are_match_results_poor(x, won)
                #Stats?
                print player_num
                msg = ResponseLast.match_performance_template.format(
                                                            hero=data.get_hero_name(x["hero_id"])["localized_name"],
                                                            k=x["kills"],
                                                            d=x["deaths"],
                                                            a=x["assists"],
                                                            GPM=x["gold_per_min"],
                                                            level=x["level"]
                                                            )
                out += msg + "\n"

                #Items?
                finalItems = "Your items: "
                for itemNum in range(0, 6):
                    if x["item_" + str(itemNum)] != 0 and x["item_" + str(itemNum)] is not None:
                        finalItems += str(data.get_item_name(x["item_" + str(itemNum)])["name"]) + ", "
                out += finalItems + "\n"

                #Win?
                #@todo fix this to incorporate woody's bugfix
                if won:
                    out += "You Won! "
                else:
                    out += "You Lost.... Bitch "
                if results_are_poor:
                    out += "Good job creating space\n"
                out += str(match_id) + " " + dotabuff_link
                return out
            player_num = player_num + 1

    @classmethod
    def are_match_results_poor(cls, player_results, won):
        if won:
            return False
        k = player_results['kills']
        d = player_results['deaths']
        a = player_results['assists']
        gpm = player_results['gold_per_min']
        xpm = player_results['xp_per_min']

        if d > (k + a) and xpm < 200:
            return True

        pprint.pprint(player_results)
        return False