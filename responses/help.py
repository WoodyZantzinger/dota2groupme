# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseHelp(AbstractResponse):

    RESPONSE_KEY = "#help"

    def __init__(self, msg, sender):
        super(ResponseHelp, self).__init__(msg, sender)