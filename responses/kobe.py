# -*- coding: utf-8 -*
from CooldownResponse import *
from random import randint


class kobe(ResponseCooldown):

    message = "#kobe"

    RESPONSE_KEY = "#kobe"

    NAMES_1 = ["dick", "penis"]

    NAMES_10 = ["liz", "erika", "paulina"]

    kobe_url = [
        "http://i.imgur.com/thhgY.gifv",
        "http://i.imgur.com/dECdK.gifv",
        "http://i.imgur.com/hr8r3.gifv",
        "http://i.imgur.com/Sv9tv.gifv",
        "http://i.imgur.com/qIJB5.gifv",
        "http://i.imgur.com/QYVa6.gifv",
        "http://i.imgur.com/G3b53.gifv",
        "http://i.imgur.com/7cB7V.gifv",
        "http://i.imgur.com/uUpX3.gifv",
        "http://i.imgur.com/eTCwx.gifv"  # 10
    ]

    COOLDOWN = 1 * 60 * 60 / 2

    def __init__(self, msg):
        super(kobe, self).__init__(msg, self.__module__, kobe.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            out = None
            names10_in_msg = [name for name in kobe.NAMES_10 if name in self.msg.text.lower()]
            if len(names10_in_msg):
                out = kobe.kobe_url[-1]
            names1_in_msg = [name for name in kobe.NAMES_1 if name in self.msg.text.lower()]
            if len(names1_in_msg):
                out = kobe.kobe_url[0]
            out = kobe.kobe_url[randint(0, len(kobe.kobe_url) - 1)]
            self.note_response(out)
            return out
        print("not responding to kobe because sender {} is on cooldown".format(self.msg.name))


