# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseSetSteam(AbstractResponse):

    RESPONSE_KEY = "#setsteam"

    def __init__(self, msg, sender):
        super(ResponseSetSteam, self).__init__(msg, sender)