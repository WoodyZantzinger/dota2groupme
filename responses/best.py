# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
from dota2py import data


class Best(AbstractResponse):

    message = "#best 1"

    RESPONSE_KEY = "#best"

    def __init__(self, msg, sender):
        Best.message = msg
        super(Best, self).__init__(msg, sender)

    def respond(self):
        out = ""

        try:
            hero_num = int(Best.message.split()[1])
            hero_name = data.get_hero_name(hero_num)["localized_name"]
            record = AbstractResponse.get_record(hero_num)
            if record is not None:
                out = "Most Kills with {0} : {1} by {2}\n".format(hero_name, record["max_kills"], AbstractResponse.dotaID_to_name(record["max_kills_player"]))
                out += "Highest GPM with {0} : {1} by {2}\n".format(hero_name, record["max_GPM"], AbstractResponse.dotaID_to_name(record["max_GPM_player"]))
                out += "Highest XPM with {0} : {1} by {2}\n".format(hero_name, record["max_XPM"], AbstractResponse.dotaID_to_name(record["max_XPM_player"]))
        except ValueError:
            out = 'Invalid value! Need Hero IDs'

        return out


