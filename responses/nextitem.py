# -*- coding: utf-8 -*
from .AbstractResponse import AbstractResponse
from dota2py import data
import random


class ResponseNextItem(AbstractResponse):

    RESPONSE_KEY = "#nextitem"

    HELP_RESPONSE = "Your next item to buy"

    def __init__(self, msg):
        super(ResponseNextItem, self).__init__(msg)

    def _respond(self):
        return "You will buy: " + ResponseNextItem.random_item()

    @classmethod
    def random_item(cls):
        next_item = data.get_item_name(random.randint(1, 212))
        if next_item is not None:
            return str(next_item["name"])
        else:
            return ResponseNextItem.next_item()