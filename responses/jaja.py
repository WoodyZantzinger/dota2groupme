# -*- coding: utf-8 -*

from CooldownResponse import *
import random


class ResponseJaJa(ResponseCooldown):

    COOLDOWN = 1 * 60 * 60 / 4

    def __init__(self, msg):
        super(ResponseJaJa, self).__init__(msg, self.__module__, ResponseJaJa.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            n = 1
            while (random.choice([0, 1])):
                n += 1
            out = "fuck andy " * n
            self.note_response(out)
            print("trying to send : " + out)
            return out
        print("not responding to jaja because sender {} is on cooldown".format(self.msg.name))

        return "Get a job"

    @classmethod
    def is_relevant_msg(cls, msg):
        return "jaja" in msg.text.lower()
