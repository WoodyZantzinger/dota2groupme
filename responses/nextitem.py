# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseNextItem(AbstractResponse):

    RESPONSE_KEY = "#nextitem"

    def __init__(self, msg, sender):
        super(ResponseNextItem, self).__init__(msg, sender)