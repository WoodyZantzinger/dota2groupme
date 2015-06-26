# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
import random


class ResponseNumbers(AbstractResponse):

    OVERRIDE_PRIORITY = 4

    NUMBERS_THRESHOLD = 6

    def __init__(self, msg, sender):
        super(ResponseNumbers, self).__init__(msg, sender)

    def respond(self):
        return "whatcha got there, numbers?"

    @classmethod
    def is_relevant_msg(cls, msg, sender):
        could_be_url = "http" in msg or "www" in msg or ".com" in msg
        not_self = sender != "sUN-self"
        n_nums = sum([_ in "1234567890" for _ in msg])
        enough_numbers = n_nums >= ResponseNumbers.NUMBERS_THRESHOLD
        booleans = not_self and enough_numbers and not could_be_url
        return booleans

