# -*- coding: utf-8 -*
from .AbstractResponse import *
from .CooldownResponse import *
import random

prophecy = []
with open(os.path.join("utils", "prophecy.txt"), encoding="utf-8") as f:
    prophecy = [line.rstrip('\n') for line in f]


class ResponseProphecy(ResponseCooldown):

    RESPONSE_KEY = "#prophecy"

    COOLDOWN = 1 * 60 * 60 / 4

    def __init__(self, msg):
        super(ResponseProphecy, self).__init__(msg, self, ResponseProphecy.COOLDOWN)

    def _respond(self):
        out = random.choice(prophecy)
        return out
