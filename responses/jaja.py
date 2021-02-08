# -*- coding: utf-8 -*

from .CooldownResponse import *
import random


class ResponseJaJa(ResponseCooldown):

    COOLDOWN = 1 * 60 * 60 / 4

    def __init__(self, msg):
        super(ResponseJaJa, self).__init__(msg, self, ResponseJaJa.COOLDOWN)

    def _respond(self):
        n = 1
        while (random.choice([0, 1])):
            n += 1
        out = "fuck andy " * n
        print("trying to send : " + out)
        return out


    @classmethod
    def is_relevant_msg(cls, msg):
        return "jaja" in msg.text.lower()
