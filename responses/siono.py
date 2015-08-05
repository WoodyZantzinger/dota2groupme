# -*- coding: utf-8 -*

from CooldownResponse import *
import random


class ResponseSiONo(ResponseCooldown):

    RESPONSE_KEY = u"#\xbf"

    COOLDOWN = 1 * 60 * 60 / 2

    def __init__(self, msg):
        super(ResponseSiONo, self).__init__(msg, self.__module__, ResponseSiONo.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            out = None
            if "omni" in self.msg.text.lower():
                out = "no"
            else:
                out = random.choice([u"sí :tacotaco:", u"no :tacotaco:"])
            self.note_response(out)
            return out
        print("not responding to siono because sender {} is on cooldown".format(self.sender))

