# -*- coding: utf-8 -*
from .AbstractResponse import *
from threading import Thread
from dota2py import api
from dota2py import data
import time


class Update(AbstractResponse):

    RESPONSE_KEY = "#update"

    message = "#update 1111111"

    HELP_RESPONSE = "Update ones's last games"

    ENABLED = False

    def __init__(self, msg):
        super(Update, self).__init__(msg)

    def respond(self):
        print("Starting")

        # Use the Thread if we are going to be updating like 1,000 records, shouldn't be needed.
        #
        #thread = Thread(target = Update.update_dota, args = (self, ))
        #thread.start()
        #
        record = self.update_dota()
        return record

    def update_dota(self):
         # Get a list of recent matches for the player
        total_added = 0
        api.set_api_key(AbstractResponse.key)
        current_time = int(time.time())
        last_update_time = AbstractResponse.get_last_update_time()
        new_records = ""
        for name, account_id in AbstractResponse.GroupMetoDOTA.items():
            print("Starting: {0}".format(name))
            # Get a list of recent matches for the player

            matches = api.get_match_history(account_id=account_id)["result"]["matches"]

            #Go through every match
            for match in matches:
                print("\tChecking: " + str(match["match_id"]))

                if match["start_time"] < last_update_time["last_update"]:
                    print("\tWe've seen these matches")
                    break

                if (not AbstractResponse.has_dotaMatch(match["match_id"])):
                    single_match = api.get_match_details(match["match_id"])["result"]
                    print("\t\tAdding: " + str(single_match["match_id"]))
                    AbstractResponse.add_dotaMatch(single_match)
                    total_added += 1

                    #Did this match set any new records# ?
                    for player in single_match["players"]:
                        #Is this a player we are tracking?
                        if AbstractResponse.has_dotaID_num(int(player["account_id"])):
                            #Yes! Check if they broke a record
                            old_record = AbstractResponse.get_record(player["hero_id"])
                            print(player["hero_id"])
                            hero_dict = data.get_hero_name(player["hero_id"])
                            if not hero_dict:
                                print("For hero id = {}, not in dota2py".format(player["hero_id"]))
                                continue
                            hero_name = data.get_hero_name(player["hero_id"])["localized_name"]
                            player_name = AbstractResponse.dotaID_to_name(int(player["account_id"]))

                            if old_record is None:

                                #this is auto a new record!
                                new_record = {"hero_id": player["hero_id"],
                                              "max_kills": player["kills"],
                                              "max_kills_player": player["account_id"],
                                              "max_deaths": player["deaths"],
                                              "max_deaths_player": player["account_id"],
                                              "max_GPM": player["gold_per_min"],
                                              "max_GPM_player": player["account_id"],
                                              "min_GPM": player["gold_per_min"],
                                              "min_GPM_player": player["account_id"],
                                              "max_XPM": player["xp_per_min"],
                                              "max_XPM_player": player["account_id"],
                                              "min_XPM": player["xp_per_min"],
                                              "min_XPM_player": player["account_id"],
                                              }
                                AbstractResponse.set_record(new_record)

                            else:
                                #There is an existing record.. Lets see if this match was a game changer
                                new_record = old_record.copy()

                                if old_record["max_kills"] < player["kills"]:
                                    new_records += "{0} just got {1} kills with {2}, a new record!\n".format(player_name, player["kills"], hero_name )
                                    new_record["max_kills"] = player["kills"]
                                    new_record["max_kills_player"] = player["account_id"]

                                if old_record["max_deaths"] < player["deaths"]:
                                    new_records += "{0} just got {1} deaths with {2}, a new low!\n".format(player_name, player["deaths"], hero_name )
                                    new_record["max_deaths"] = player["deaths"]
                                    new_record["max_deaths_player"] = player["account_id"]

                                if old_record["max_GPM"] < player["gold_per_min"]:
                                    new_records += "{0} just got {1} GPM with {2}, a new record!\n".format(player_name, player["gold_per_min"], hero_name )
                                    new_record["max_GPM"] = player["gold_per_min"]
                                    new_record["max_GPM_player"] = player["account_id"]

                                if old_record["min_GPM"] > player["gold_per_min"]:
                                    new_records += "{0} just got {1} GPM with {2}, a new low!\n".format(player_name, player["gold_per_min"], hero_name )
                                    new_record["min_GPM"] = player["gold_per_min"]
                                    new_record["min_GPM_player"] = player["account_id"]

                                if old_record["max_XPM"] < player["xp_per_min"]:
                                    new_records += "{0} just got {1} XPM with {2}, a new record!\n".format(player_name, player["xp_per_min"], hero_name )
                                    new_record["max_XPM"] = player["xp_per_min"]
                                    new_record["max_XPM_player"] = player["account_id"]

                                if old_record["min_XPM"] > player["xp_per_min"]:
                                    new_records += "{0} just got {1} XPM with {2}, a new low!\n".format(player_name, player["xp_per_min"], hero_name )
                                    new_record["min_XPM"] = player["xp_per_min"]
                                    new_record["min_XPM_player"] = player["account_id"]

                                AbstractResponse.set_record(new_record)

                else:
                    print("\t Was Duplicate")

            print("Updated {0} Matches".format(total_added))
        if last_update_time == None:
            time_dict = {'last_update' : current_time}
        else:
            time_dict = last_update_time.copy()
            time_dict["last_update"] = current_time
        AbstractResponse.set_last_update_time(time_dict)
        return new_records
