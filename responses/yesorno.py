# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
import random


class ResponseYesOrNo(AbstractResponse):

    RESPONSE_KEY = "#yesorno"

    def __init__(self, msg, sender):
        super(ResponseYesOrNo, self).__init__(msg, sender)

    def respond(self):
        return random.choice(["yes", "no"])

