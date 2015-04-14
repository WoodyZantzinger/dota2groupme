# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
from dota2py import data


class Worst(AbstractResponse):

    message = "#worst 1"
    
    SPECIFIC_RESPONSES = {"person": "Jon",
                            "beer": "Mother. Fucking. Pabst.",
                            "game": "Hello Kitty Adventure, Pink Edition",
                            "friend": "Porcupines"
                            "country": "Canada (sike prolly some Middle East place)"
                            "food": "Anything with blue cheese",
                            "liquor": "I hardly even know 'er"
                            "bear": "Koala"
                            "chicken": "KFC"}

    RESPONSE_KEY = "#worst"

    def __init__(self, msg, sender):
        Worst.message = msg
        super(Worst, self).__init__(msg, sender)

    def respond(self):

        out = ""
        hero_name = Worst.message.split(' ', 1)
        if len(hero_name) < 2:
            out = "You need a hero name"
        else:

            hero_num = AbstractResponse.get_hero_id(hero_name[1])
            if hero_num < 0:
                name = hero_name[1].lower()
                if name in Worst.SPECIFICRESPONSES:
                    out = Best.SPECIFIC_RESPONSES[name]
                else:
                    out = "Hero not found"
            else:
                hero_name = data.get_hero_name(hero_num)["localized_name"]
                record = AbstractResponse.get_record(hero_num)
                if record is not None:
                    out = "Most Deaths with {0} : {1} by {2}\n".format(hero_name, record["max_deaths"], AbstractResponse.dotaID_to_name(record["max_deaths_player"]))
                    out += "Lowest GPM with {0} : {1} by {2}\n".format(hero_name, record["min_GPM"], AbstractResponse.dotaID_to_name(record["min_GPM_player"]))
                    out += "Lowest XPM with {0} : {1} by {2}\n".format(hero_name, record["min_XPM"], AbstractResponse.dotaID_to_name(record["min_XPM_player"]))
        return out


