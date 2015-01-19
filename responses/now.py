# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseNow(AbstractResponse):

    RESPONSE_KEY = "#now"

    def __init__(self, msg, sender):
        super(ResponseNow, self).__init__(msg, sender)