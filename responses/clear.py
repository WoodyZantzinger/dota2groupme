# -*- coding: utf-8 -*
from .AbstractResponse import *
from .CooldownResponse import *
import random


class ResponseClear(AbstractResponse):

    RESPONSE_KEY = "#clear"



    def __init__(self, msg):
        super(ResponseClear, self).__init__(msg)

    def respond(self):
        str_number_of_lines = self.msg.text.partition(' ')[2].lower()
        number_of_lines = 10
        try:
            number_of_lines = int(str_number_of_lines)
        except ValueError:
            number_of_lines = 10

        if number_of_lines > 20: number_of_lines = 20

        out = ":dino: \n"
        for x in range(0,number_of_lines):
            out += ":dino: \n"

        return out