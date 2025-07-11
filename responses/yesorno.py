# -*- coding: utf-8 -*

from .CooldownResponse import *
import random


class ResponseYesOrNo(ResponseCooldown):

    RESPONSE_KEY = "#?"

    COOLDOWN = 1 * 60 * 60 / 2

    def __init__(self, msg):
        super(ResponseYesOrNo, self).__init__(msg, self, ResponseYesOrNo.COOLDOWN)

    def _respond(self):
        out = None
        if "omni" in self.msg.text.lower():
            out = "no"
        else:
            if random.random() < 0.01:
                out = "maybe :dino:"
            else:
                out = random.choice(["yes :dino:", "no :dino:"])
        return out

