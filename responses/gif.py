# -*- coding: utf-8 -*
from AbstractResponse import *
import requests


class gif(AbstractResponse):

    message = "#gif"

    RESPONSE_KEY = "#gif"

    url = 'http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag={term}'

    def __init__(self, msg, sender):
        gif.message = msg
        super(gif, self).__init__(msg, sender)

    def respond(self):
        out = ""
        search_term = gif.message.partition(' ')[2]

        request_url = gif.url.format(term=search_term)

        response = requests.get(request_url)

        try:
            print request_url
            out = response.json()["data"]["image_url"]
        except Exception as e:
            out = "Something went wrong"

        return out


