# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseSetSteam(AbstractResponse):

    RESPONSE_KEY = "#setsteam"

    HELP_RESPONSE = "Set your SteamID if not hardcoded in yet. This is you Steam (Not Dota) username."

    def __init__(self, msg, sender):
        super(ResponseSetSteam, self).__init__(msg, sender)

    def respond(self):
        #@TODO make this work
        #i doubt this works :(
        AbstractResponse.GroupMetoDOTA[self.sender] = self.msg
        return "I set your Steam ID to: " + self.msg