# -*- coding: utf-8 -*
from AbstractResponse import *
import requests


class gif(AbstractResponse):

    message = "#gif"

    RESPONSE_KEY = "#gif"

    url = 'http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag={term}'

    def __init__(self, msg, sender):
        super(gif, self).__init__(msg, sender)

    def respond(self):
        out = ""
        search_term = self.msg.partition(' ')[2]

        request_url = gif.url.format(term=search_term)

        response = requests.get(request_url)

        try:
            print request_url
            out = response.json()["data"]["image_url"]
        except Exception:
            out = "Something went wrong"

        if self.sender in ["Andy Esposito"]:
            return "http://media.giphy.com/media/bRmVNYlTLX9e0/giphy.gif"
        return out

    @classmethod
    def is_relevant_msg(cls, msg, sender):
        return not sender in ["Andy Esposito"] and gif.RESPONSE_KEY in msg



