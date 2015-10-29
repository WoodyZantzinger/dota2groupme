# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseStatus(AbstractResponse):

    RESPONSE_KEY = "#status"

    HELP_RESPONSE = "See if sUN bot is up"

    def __init__(self, msg, sender):
        super(ResponseStatus, self).__init__(msg, sender)

    def respond(self):
        return "Currently listening ;)"