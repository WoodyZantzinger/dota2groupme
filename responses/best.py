# -*- coding: utf-8 -*
from AbstractResponse import *
from dota2py import data


class Best(AbstractResponse):

    message = "#best 1"

    RESPONSE_KEY = "#best"

    def __init__(self, msg, sender):
        Best.message = msg
        super(Best, self).__init__(msg, sender)

    def respond(self):
        out = ""
        hero_name = Best.message.split(' ', 1)
        if len(hero_name) < 2:
            out = "You need a hero name"
        else:

            hero_num = AbstractResponse.get_hero_id(hero_name[1])
            if hero_num < 0:
                if hero_name[1] == "person":
                    out = "Woody"
                elif hero_name[1] == "beer":
                    out = "Budweiser"
                elif hero_name[1] == "game":
                    out = "The Dota"
                elif hero_name[1] == "friend":
                    out = "Beer"
                elif hero_name[1] == "country":
                    out = "USA!"
                else:
                    out = "Hero not found"
            else:
                hero_name = data.get_hero_name(hero_num)["localized_name"]
                record = AbstractResponse.get_record(hero_num)
                if record is not None:
                    out = "Most Kills with {0} : {1} by {2}\n".format(hero_name, record["max_kills"], AbstractResponse.dotaID_to_name(record["max_kills_player"]))
                    out += "Highest GPM with {0} : {1} by {2}\n".format(hero_name, record["max_GPM"], AbstractResponse.dotaID_to_name(record["max_GPM_player"]))
                    out += "Highest XPM with {0} : {1} by {2}\n".format(hero_name, record["max_XPM"], AbstractResponse.dotaID_to_name(record["max_XPM_player"]))
        return out


