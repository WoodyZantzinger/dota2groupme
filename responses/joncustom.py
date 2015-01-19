# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseJonCustom(AbstractResponse):

    OVERRIDE_PRIORITY = 5

    def __init__(self, msg, sender):
        super(ResponseJonCustom, self).__init__(msg, sender)

    def respond(self):
        return "8======D"

    @classmethod
    def is_relevant_msg(cls, msg, sender):
        return sender in ["Jonny G"]

