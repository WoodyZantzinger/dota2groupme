# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
import random


class ResponseSassyOverride(AbstractResponse):

    INSULT_THRESHOLD = 0.005

    OVERRIDE_PRIORITY = 5

    mean_names = ["bitch", "loser", "jabroni", "fudgepacker", "dipshit", "idiot", "assjacker", "axwound", "boner",
                  "butt-pirate", "cockface", "dickbag", "fuckstick", "jackass", "muffdiver", "prick", "queef", "rimjob",
                  "shitstain", "thundercunt", "unclefucker"]

    def __init__(self, msg, sender):
        super(ResponseSassyOverride, self).__init__(msg, sender)

    def respond(self):
        return "No, you {}".format(random.choice(ResponseSassyOverride.mean_names))

    @classmethod
    def is_relevant_msg(cls, msg, sender):
        relevant_to_me = "?" in msg or "#" in msg
        could_be_url = "http" in msg or "www" in msg or ".com" in msg
        return random.random() < ResponseSassyOverride.INSULT_THRESHOLD and relevant_to_me and not could_be_url

