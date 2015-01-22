# -*- coding: utf-8 -*
from AbstractResponse import *
from dota2py import api
from dota2py import data

class ResponseLast(AbstractResponse):

    match_performance_template = "As {hero} you went {k}:{d}:{a} with {GPM} GPM finishing at level {level}"

    RESPONSE_KEY = "#update"

    HELP_RESPONSE = "Update everyones last games"

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

        #Go through every match, store in database with every user we know

        for match in matches:

            single_match = api.get_match_details(match["match_id"])

            out = ""
            player_num = 0
            for x in single_match["result"]["players"]:
                if AbstractResponse.has_dotaID_num(int(x["account_id"])):
                    out += AbstractResponse.dotaID_to_name(int(x["account_id"])) + "\n"
                    #print "We know this user!"

                    #Stats?
                    #print player_num
                    print x["hero_id"]

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
                            finalItems += str(data.get_item_name(x["item_" + str(itemNum)])["name"]) + ", "
                    out += finalItems + "\n"
                player_num = player_num + 1

            if player_num < 5 and single_match["result"]["radiant_win"]:
                out += "You Won!" + "\n"
            elif player_num > 4 and not single_match["result"]["radiant_win"]:
                out += "You Won!" + "\n"
            else:
                out += "You Lost.... Bitch"
            print out
        print "\n"
        return 'OK'
