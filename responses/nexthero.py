# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
from dota2py import data
import random


class ResponseNext(AbstractResponse):

    RESPONSE_KEY = "#next"

    HELP_RESPONSE = "Your next hero to play"

    def __init__(self, msg):
        super(ResponseNext, self).__init__(msg)

    def respond(self):
        return "You will play: " + ResponseNext.random_hero()

    @classmethod
    def is_relevant_msg(cls, msg):
        return ResponseNext.RESPONSE_KEY in msg.text.lower() and "#nextteam" not in msg.text and "#nextitem" not in msg.text

    @classmethod
    def random_hero(cls):
        #@TODO should not hardcode  limits of random
        next_hero = data.get_hero_name(random.randint(1, 107))
        if next_hero is not None:
            return str(next_hero["localized_name"])
        else:
            return ResponseNext.random_hero()