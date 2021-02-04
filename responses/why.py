# -*- coding: utf-8 -*
from .AbstractResponse import *
from .CooldownResponse import *
import random

reasons = []
with open(os.path.join("utils", "reasons.txt")) as f:
    reasons = [line.rstrip('\n') for line in f]


class ResponseWhy(ResponseCooldown):

    RESPONSE_KEY = "#why"

    COOLDOWN = 1 * 60 * 60 / 4

    def __init__(self, msg):
        super(ResponseWhy, self).__init__(msg, self, ResponseWhy.COOLDOWN)

    def _respond(self):
        if self.is_sender_off_cooldown():
            out = random.choice(reasons)
            self.note_response(out)
            return out
        else:
            print("not responding to #why because sender {} is on cooldown".format(self.msg.name))