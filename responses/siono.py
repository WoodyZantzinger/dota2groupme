# -*- coding: utf-8 -*

from .CooldownResponse import *
import random


class ResponseSiONo(ResponseCooldown):

    RESPONSE_KEY = u"#\xbf"

    COOLDOWN = 1 * 60 * 60 / 2

    def __init__(self, msg):
        super(ResponseSiONo, self).__init__(msg, self, ResponseSiONo.COOLDOWN)

    def _respond(self):
        out = None
        if "omni" in self.msg.text.lower():
            out = "no"
        else:
            out = random.choice(["si :tacotaco:", "no :tacotaco:"])
        return out

