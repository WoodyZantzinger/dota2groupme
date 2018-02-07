# -*- coding: utf-8 -*
from AbstractResponse import *
from CooldownResponse import *
import random

moves = []

with open(os.path.join(os.path.dirname(__file__), '../utils/moves.txt')) as f:
    moves = [line.rstrip('\n') for line in f]


class ResponseAttack(ResponseCooldown):

    RESPONSE_KEY = "#attack"

    COOLDOWN = 1 * 60 * 60 / 4

    def __init__(self, msg):
        super(ResponseAttack, self).__init__(msg, self.__module__, ResponseAttack.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            out = random.choice(moves)
            self.note_response(out)
            return out
        else:
            print("not responding to #attack because sender {} is on cooldown".format(self.msg.name))