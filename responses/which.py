# -*- coding: utf-8 -*
from AbstractResponse import *
import random
from CooldownResponse import *


class ResponseWhich(ResponseCooldown):

    RESPONSE_KEY = "#which"

    COOLDOWN = 10 * 60

    def __init__(self, msg):
        super(ResponseWhich, self).__init__(msg, self.__module__, ResponseWhich.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            start = self.msg.text.find("(")
            end = self.msg.text[start:].find(")")
            whiches = self.msg.text[start + 1:start + end].split(",")
            out = random.choice(whiches)
            self.note_response(out)
            return out
        else:
            print("not responding to #what because sender {} is on cooldown".format(self.msg.name))
