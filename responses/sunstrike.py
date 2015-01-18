# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseSunstrike(AbstractResponse):

    RESPONSE_KEY = "#sunstrike"

    def __init__(self, msg, sender):
        super(ResponseSunstrike, self).__init__(msg, sender)