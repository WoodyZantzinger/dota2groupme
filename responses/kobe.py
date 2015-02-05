# -*- coding: utf-8 -*
from AbstractResponse import *
import requests
from random import randint

class kobe(AbstractResponse):

    message = "#kobe"

    RESPONSE_KEY = "#kobe"

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
        "http://i.imgur.com/eTCwx.gif"
    ]

    def __init__(self, msg, sender):
        kobe.message = msg
        super(kobe, self).__init__(msg, sender)

    def respond(self):
        return kobe.kobe_url[randint(0,9)]


