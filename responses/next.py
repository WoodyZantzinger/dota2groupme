# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseNext(AbstractResponse):

    RESPONSE_KEY = "#next"

    def __init__(self, msg, sender):
        super(ResponseNext, self).__init__(msg, sender)