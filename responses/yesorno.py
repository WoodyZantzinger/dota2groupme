# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
from CooldownResponse import *
import random


class ResponseYesOrNo(ResponseCooldown):

    RESPONSE_KEY = "#?"

    COOLDOWN = 1 * 60 * 60 / 2

    def __init__(self, msg, sender):
        super(ResponseYesOrNo, self).__init__(msg, sender, self.__module__, ResponseYesOrNo.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            if "omni" in self.msg.lower():
                return "no"
            return random.choice(["yes", "no"])
        print("not responding to yesorno because sender {} is on cooldown".format(self.sender))

