# -*- coding: utf-8 -*

from CooldownResponse import *
import random


class ResponseWhich(ResponseCooldown):

    RESPONSE_KEY = "#which"

    COOLDOWN = 1 * 60 * 60 / 4

    def __init__(self, msg):
        super(ResponseWhich, self).__init__(msg, self.__module__, ResponseWhich.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            words = self.msg.text.split(" ")[1:]
            out = random.choice(words)
            self.note_response(out)
            return out
        print("not responding to which because sender {} is on cooldown".format(self.sender))

