# -*- coding: utf-8 -*
from .AbstractResponse import *
import random
from .CooldownResponse import *


class ResponseWhich(ResponseCooldown):

    RESPONSE_KEY = "#which"

    COOLDOWN = 10 * 60

    def __init__(self, msg):
        super(ResponseWhich, self).__init__(msg, self, ResponseWhich.COOLDOWN)

    def _respond(self):
        start = self.msg.text.find("(")
        end = self.msg.text[start:].find(")")
        whiches = self.msg.text[start + 1:start + end].split(",")
        out = random.choice(whiches)
        return out
