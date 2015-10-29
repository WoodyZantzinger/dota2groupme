# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseFishstick(AbstractResponse):

    OVERRIDE_PRIORITY = 4

    def __init__(self, msg):
        super(ResponseFishstick, self).__init__(msg)

    def respond(self):
        return "{}, you a gay fish".format(self.msg.name)

    @classmethod
    def is_relevant_msg(cls, msg):
        return 'fishstick' in msg.text.lower() or 'fish stick' in msg.text.lower()

