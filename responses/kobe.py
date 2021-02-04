# -*- coding: utf-8 -*
from .CooldownResponse import *
from random import randint


class kobe(ResponseCooldown):

    message = "#kobe"

    RESPONSE_KEY = "#kobe"

    NAMES_1 = ["dick", "penis"]

    NAMES_10 = ["liz", "erika", "paulina", "nat", "natalie", "lynds", "lyndsey", "chelsea"]

    kobe_url = [
        "http://i.imgur.com/thhgY.gif",
    ]

    COOLDOWN = 1 * 60 * 60 / 2

    def __init__(self, msg):
        super(kobe, self).__init__(msg, self, kobe.COOLDOWN)

    def _respond(self):
        if self.is_sender_off_cooldown():
            out = None
            # kobe was #1
            out = kobe.kobe_url[0]
            self.note_response(out)
            return out
        print("not responding to kobe because sender {} is on cooldown".format(self.msg.name))


