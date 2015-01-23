# -*- coding: utf-8 -*
from AbstractResponse import *
from dota2py import api
from dota2py import data

class ResponseLast(AbstractResponse):

    RESPONSE_KEY = "#update"

    HELP_RESPONSE = "Update everyone's last games"

    def __init__(self, msg, sender):
        super(ResponseLast, self).__init__(msg, sender)

    def respond(self):

        print "Starting"

        total_added = 0

        api.set_api_key(AbstractResponse.key)

        #For every user
        for name, account_id in AbstractResponse.GroupMetoDOTA.items():
            print "Starting: {0}".format(name)
            # Get a list of recent matches for the player
            matches = api.get_match_history(account_id=account_id)["result"]["matches"]

            #Go through every match
            for match in matches:

                single_match = api.get_match_details(match["match_id"])["result"]
                print "Checking: " + str(single_match["match_id"])

                if (not AbstractResponse.has_dotaMatch(single_match["match_id"])):
                    print "\t Adding: " + str(single_match["match_id"])
                    AbstractResponse.add_dotaMatch(single_match)
                    total_added += 1
                else:
                    print "\t Was Duplicate"
        final_string = "Updated {0} Matches".format(total_added)
        return final_string
