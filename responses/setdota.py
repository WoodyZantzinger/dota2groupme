# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseSetDota(AbstractResponse):

    RESPONSE_KEY = "#setdota"

    HELP_RESPONSE = "This is your Dota ID number. Find this as the last number in your DotaBuff URL"

    def __init__(self, msg):
        super(ResponseSetDota, self).__init__(msg)

    def respond(self):
        #@TODO make this work
        #i doubt this works :(
        canonical_name = (key for key,value in AbstractResponse.GroupMeIDs.items() if value==self.msg.sender_id).next()
        AbstractResponse.GroupMetoDOTA[canonical_name] = self.msg.name
        return "I set your Dota ID to: " + self.msg.name