# -*- coding: utf-8 -*

from CooldownResponse import *
import random


class ResponseYesOrNo(ResponseCooldown):

    RESPONSE_KEY = "#?"

    COOLDOWN = 1 * 60 * 60 / 2

    def __init__(self, msg):
        super(ResponseYesOrNo, self).__init__(msg, self.__module__, ResponseYesOrNo.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            out = None
            if "omni" in self.msg.text.lower():
                out = "no"
            else:
                out = random.choice(["yes", "no"])
            self.note_response(out)
            return out
        print("not responding to yesorno because sender {} is on cooldown".format(self.sender))

