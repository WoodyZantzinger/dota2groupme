# -*- coding: utf-8 -*

from .CooldownResponse import *

class ResponseLol(ResponseCooldown):

    COOLDOWN = 1 * 60 * 60 / 2
    NOTED_RESPONSE = None
    RESPONSE_TOTAL = 0
    RESPONSE_THRESHOLD = 3

    def __init__(self, msg):
        super(ResponseLol, self).__init__(msg, self, ResponseLol.COOLDOWN)

    def _respond(self):
        out = ResponseLol.NOTED_RESPONSE
        return out

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
