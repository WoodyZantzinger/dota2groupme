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
        super(ResponseWhat, self).__init__(msg, self.__module__, ResponseWhat.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            out = random.choice(things)
            self.note_response(out)
            return out
        else:
            print("not responding to #what because sender {} is on cooldown".format(self.msg.name))