# -*- coding: utf-8 -*
from .AbstractResponse import AbstractResponse


class ResponseJonCustom(AbstractResponse):

    OVERRIDE_PRIORITY = 5

    ENABLED = False

    def __init__(self, msg):
        super(ResponseJonCustom, self).__init__(msg)

    def _respond(self):
        return "8======D"

    @classmethod
    def is_relevant_msg(cls, msg):
        return (msg.sender_id == AbstractResponse.GroupMeIDs['Jonny G'])

