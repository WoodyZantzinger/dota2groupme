# -*- coding: utf-8 -*
from .AbstractResponse import AbstractResponse


class ResponseSetSteam(AbstractResponse):

    RESPONSE_KEY = "#setsteam"

    HELP_RESPONSE = "Set your SteamID if not hardcoded in yet. This is you Steam (Not Dota) username."

    def __init__(self, msg):
        super(ResponseSetSteam, self).__init__(msg)

    def respond(self):
        #@TODO make this work
        #i doubt this works :(
        canonical_name = (key for key,value in AbstractResponse.GroupMeIDs.items() if value==self.msg.sender_id).next()
        AbstractResponse.GroupMetoDOTA[canonical_name] = self.msg.name
        return "I set your Steam ID to: " + self.msg.name