# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
import random


class ResponseSassyOverride(AbstractResponse):

    INSULT_THRESHOLD = 0.005

    OVERRIDE_PRIORITY = 5

    mean_names = ["bitch", "loser", "jabroni", "fudgepacker", "dipshit", "idiot", "assjacker", "axwound", "boner",
                  "butt-pirate", "cockface", "dickbag", "fuckstick", "jackass", "muffdiver", "prick", "queef", "rimjob",
                  "shitstain", "thundercunt", "unclefucker","chickenfucker","taint licker","gaping cock-socket","fat fuck"]

    def __init__(self, msg):
        super(ResponseSassyOverride, self).__init__(msg)

    def respond(self):
        return "No, you {}".format(random.choice(ResponseSassyOverride.mean_names))

    @classmethod
    def is_relevant_msg(cls, msg):
        relevant_to_me = "?" in msg.text or "#" in msg.text
        could_be_url = "http" in msg.text or "www" in msg.text or ".com" in msg.text
        not_self = msg.sender_id != AbstractResponse.GroupMeIDs["sUN"]
        booleans = relevant_to_me and not could_be_url and not_self
        return random.random() < ResponseSassyOverride.INSULT_THRESHOLD and booleans

