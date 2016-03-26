# -*- coding: utf-8 -*
from AbstractResponse import *
from random import randint


class kobe(AbstractResponse):

    message = "#kobe"

    RESPONSE_KEY = "#kobe"

    NAMES_1 = ["dick", "penis"]

    NAMES_10 = ["liz", "erika", "paulina"]

    kobe_url = [
        "http://i.imgur.com/thhgY.gif",
        "http://i.imgur.com/dECdK.gif",
        "http://i.imgur.com/hr8r3.gif",
        "http://i.imgur.com/Sv9tv.gif",
        "http://i.imgur.com/qIJB5.gif",
        "http://i.imgur.com/QYVa6.gif",
        "http://i.imgur.com/G3b53.gif",
        "http://i.imgur.com/7cB7V.gif",
        "http://i.imgur.com/uUpX3.gif",
        "http://i.imgur.com/eTCwx.gif"  # 10
    ]

    def __init__(self, msg):
        super(kobe, self).__init__(msg)

    def respond(self):
        names10_in_msg = [name for name in kobe.NAMES_10 if name in self.msg.text.lower()]
        if len(names10_in_msg):
            return kobe.kobe_url[-1]
        names1_in_msg = [name for name in kobe.NAMES_1 if name in self.msg.text.lower()]
        if len(names1_in_msg):
            return kobe.kobe_url[0]
        return kobe.kobe_url[randint(0, len(kobe.kobe_url) - 1)]


