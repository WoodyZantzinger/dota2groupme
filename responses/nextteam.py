# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseNextTeam(AbstractResponse):

    RESPONSE_KEY = "#nextteam"

    def __init__(self, msg, sender):
        super(ResponseNextTeam, self).__init__(msg, sender)