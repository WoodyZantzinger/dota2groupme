# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
from dota2py import data
import random

class ResponseNext(AbstractResponse):

    RESPONSE_KEY = "#next"

    def __init__(self, msg, sender):
        super(ResponseNext, self).__init__(msg, sender)

    def respond(self):
        return "You will play: " + ResponseNext.random_hero()

    @classmethod
    def random_hero(cls):
        next_hero = data.get_hero_name(random.randint(1, 107))
        if next_hero is not None:
            return str(next_hero["localized_name"])
        else:
            return ResponseNext.random_hero()