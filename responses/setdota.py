# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseSetDota(AbstractResponse):

    RESPONSE_KEY = "#setdota"

    HELP_RESPONSE = "This is your Dota ID number. Find this as the last number in your DotaBuff URL"

    def __init__(self, msg, sender):
        super(ResponseSetDota, self).__init__(msg, sender)

    def respond(self):
        #@TODO make this work
        #i doubt this works :(
        AbstractResponse.GroupMetoDOTA[self.sender] = self.msg
        return "I set your Dota ID to: " + self.msg