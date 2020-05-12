# -*- coding: utf-8 -*
from .AbstractResponse import AbstractResponse


class ResponseHelp(AbstractResponse):

    RESPONSE_KEY = "#help"

    HELP_RESPONSE = "Sends help information"

    def __init__(self, msg):
        super(ResponseHelp, self).__init__(msg)

    def respond(self):
        classes = AbstractResponse.__subclasses__()
        out = ""
        for cls in classes:
            if cls.RESPONSE_KEY != AbstractResponse.RESPONSE_KEY:
                out += cls.RESPONSE_KEY + " : " + cls.HELP_RESPONSE + '\n'
        return out
