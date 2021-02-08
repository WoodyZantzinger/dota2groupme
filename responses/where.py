# -*- coding: utf-8 -*
from .AbstractResponse import *
from .CooldownResponse import *
import random

places = []
with open(os.path.join("utils", "places.txt")) as f:
    places = [line.rstrip('\n') for line in f]


class ResponseWhere(ResponseCooldown):

    RESPONSE_KEY = "#where"

    COOLDOWN = 1 * 60 * 60 / 4

    def __init__(self, msg):
        super(ResponseWhere, self).__init__(msg, self, ResponseWhere.COOLDOWN)

    def _respond(self):
        out = random.choice(places)
        return out