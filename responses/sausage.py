# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseSausage(AbstractResponse):

    OVERRIDE_PRIORITY = 4

    def __init__(self, msg, sender):
        super(ResponseSausage, self).__init__(msg, sender)

    def respond(self):
        return "But, {}, you don't even have any money".format(self.sender)

    @classmethod
    def is_relevant_msg(cls, msg, sender):
        return sender in ["Brian", "Jonny G"] and 'sausage' in msg

