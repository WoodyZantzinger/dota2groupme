# -*- coding: utf-8 -*
from .AbstractResponse import *
from .CooldownResponse import *
import random

things = []
with open(os.path.join("utils", "things.txt")) as f:
    things = [line.rstrip('\n') for line in f]


class ResponseWhat(ResponseCooldown):

    RESPONSE_KEY = "#what"

    COOLDOWN = 1 * 60 * 60 / 4

    def __init__(self, msg):
        super(ResponseWhat, self).__init__(msg, self, ResponseWhat.COOLDOWN)

    def _respond(self):
        out = random.choice(things)
        return out