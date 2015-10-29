# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseResponses(AbstractResponse):

    RESPONSE_KEY = "#past"

    def __init__(self, msg):
        super(ResponseResponses, self).__init__(msg)

    def respond(self):
        parts = self.msg.text.split(" ")
        name = parts[1]
        url = "http://young-fortress-3393.herokuapp.com/past_response/{}".format(name)
        return url
