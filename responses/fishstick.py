# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseFishstick(AbstractResponse):

    OVERRIDE_PRIORITY = 4

    def __init__(self, msg, sender):
        super(ResponseFishstick, self).__init__(msg, sender)

    def respond(self):
        return "{}, you a gay fish".format(self.sender)

    @classmethod
    def is_relevant_msg(cls, msg, sender):
        return 'fishstick' in msg.lower() or 'fish stick' in msg.lower()

