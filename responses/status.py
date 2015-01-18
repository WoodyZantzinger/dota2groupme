# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseStatus(AbstractResponse):

    RESPONSE_KEY = "#status"

    def __init__(self, msg, sender):
        super(ResponseStatus, self).__init__(msg, sender)