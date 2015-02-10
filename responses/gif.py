# -*- coding: utf-8 -*
from AbstractResponse import *
from CooldownResponse import *
import requests


class ResponseGif(ResponseCooldown):

    message = "#gif"

    RESPONSE_KEY = "#gif"

    COOLDOWN = 1 * 60 * 60 * 3 / 2

    url = 'http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag={term}'

    def __init__(self, msg, sender):
        super(ResponseGif, self).__init__(msg, sender, self.__module__, ResponseGif.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            out = ""
            search_term = self.msg.partition(' ')[2]
            request_url = ResponseGif.url.format(term=search_term)
            response = requests.get(request_url)
            try:
                print request_url
                out = response.json()["data"]["image_url"]
            except Exception:
                out = "Something went wrong"

            return out
        else:
            print("not responding to gif because sender {} is on cooldown".format(self.sender))
