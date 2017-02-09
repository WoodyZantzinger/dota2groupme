# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse

# general memeing

class ResponseQeustionMark(AbstractResponse):

    OVERRIDE_PRIORITY = 4

    def __init__(self, msg):
        super(ResponseQeustionMark, self).__init__(msg)

    def respond(self):
        return "dont qeustion mark lol"

    @classmethod
    def is_relevant_msg(cls, msg):
        return msg.text =='?'



