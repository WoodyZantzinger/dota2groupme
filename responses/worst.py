# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
from dota2py import data


class Worst(AbstractResponse):

    message = "#worst 1"

    RESPONSE_KEY = "#worst"

    def __init__(self, msg, sender):
        Worst.message = msg
        super(Worst, self).__init__(msg, sender)

    def respond(self):
        out = ""

        try:
            hero_num = int(Worst.message.split()[1])
            hero_name = data.get_hero_name(hero_num)["localized_name"]
            record = AbstractResponse.get_record(hero_num)
            if record is not None:
                out = "Most Deaths with {0} : {1} by {2}\n".format(hero_name, record["max_deaths"], AbstractResponse.dotaID_to_name(record["max_deaths_player"]))
                out += "Lowest GPM with {0} : {1} by {2}\n".format(hero_name, record["min_GPM"], AbstractResponse.dotaID_to_name(record["min_GPM_player"]))
                out += "Lowest XPM with {0} : {1} by {2}\n".format(hero_name, record["min_XPM"], AbstractResponse.dotaID_to_name(record["min_XPM_player"]))
        except ValueError:
            out = 'Invalid value! Need Hero IDs'

        return out


