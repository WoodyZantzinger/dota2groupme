# -*- coding: utf-8 -*
from .AbstractResponse import *
from .CooldownResponse import *
import random

moves = []
with open(os.path.join("utils", "moves.txt")) as f:
    moves = [line.rstrip('\n') for line in f]


class ResponseAttack(ResponseCooldown):

    RESPONSE_KEY = "#attack"

    COOLDOWN = 1 * 60 * 60 / 4

    def __init__(self, msg):
        super(ResponseAttack, self).__init__(msg, self, ResponseAttack.COOLDOWN)

    def _respond(self):
        out = random.choice(moves)
        return out
