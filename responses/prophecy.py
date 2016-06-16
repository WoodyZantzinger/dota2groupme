# -*- coding: utf-8 -*
from AbstractResponse import *
from CooldownResponse import *
import random

prophecy = []
with open(os.path.join("utils", "prophecy.txt")) as f:
    prophecy = [line.rstrip('\n') for line in f]


class ResponseProphecy(ResponseCooldown):

    RESPONSE_KEY = "#prophecy"

    COOLDOWN = 1 * 60 * 60 / 4

    def __init__(self, msg):
        super(ResponseProphecy, self).__init__(msg, self.__module__, ResponseProphecy.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            out = random.choice(prophecy)
            self.note_response(out)
            return out
        else:
            print("not responding to #prophecy because sender {} is on cooldown".format(self.msg.name))
