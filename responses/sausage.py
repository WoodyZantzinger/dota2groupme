# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseSausage(AbstractResponse):

    OVERRIDE_PRIORITY = 4

    def __init__(self, msg):
        super(ResponseSausage, self).__init__(msg)

    def respond(self):
        return "But, {}, you don't even have any money".format(self.msg.name)

    @classmethod
    def is_relevant_msg(cls, msg):
        return AbstractResponse.GroupMeIDs["Jonny G"] == msg.sender_id and 'sausage' in msg.text

