# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseNumbers(AbstractResponse):

    OVERRIDE_PRIORITY = 4

    NUMBERS_THRESHOLD = 6

    ENABLED = False

    def __init__(self, msg):
       super(ResponseNumbers, self).__init__(msg)

    def respond(self):
        return "whatcha got there, numbers?"

    @classmethod
    def is_relevant_msg(cls, msg):
        could_be_url = "http" in msg.text or "www" in msg.text or ".com" in msg.text
        not_self = msg.sender_id != AbstractResponse.GroupMeIDs['sUN']
        n_nums = sum([_ in "1234567890" for _ in msg.text])
        enough_numbers = n_nums >= ResponseNumbers.NUMBERS_THRESHOLD
        booleans = not_self and enough_numbers and not could_be_url
        return booleans

