# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseSetDota(AbstractResponse):

    RESPONSE_KEY = "#setdota"

    def __init__(self, msg, sender):
        super(ResponseSetDota, self).__init__(msg, sender)