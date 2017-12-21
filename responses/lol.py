# -*- coding: utf-8 -*

from CooldownResponse import *

class ResponseLol(ResponseCooldown):

    COOLDOWN = 1 * 60 * 60 / 2
    NOTED_RESPONSE = None
    RESPONSE_TOTAL = 0
    RESPONSE_THRESHOLD = 3

    def __init__(self, msg):
        super(ResponseLol, self).__init__(msg, self.__module__, ResponseLol.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            out = ResponseLol.NOTED_RESPONSE
            self.note_response(out)
            return out
        print("not responding to jaja because sender {} is on cooldown".format(self.msg.name))

    @classmethod
    def is_relevant_msg(cls, msg):
        if msg.text.lower() != ResponseLol.NOTED_RESPONSE:
            ResponseLol.NOTED_RESPONSE = msg.text.lower()
            ResponseLol.RESPONSE_TOTAL = 1
        else:
            ResponseLol.RESPONSE_TOTAL = ResponseLol.RESPONSE_TOTAL + 1

        if ResponseLol.RESPONSE_TOTAL == ResponseLol.RESPONSE_THRESHOLD:
            ResponseLol.RESPONSE_TOTAL = 0
            return True
        else:
            return False
