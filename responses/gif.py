# -*- coding: utf-8 -*
from AbstractResponse import *
from CooldownResponse import *
import requests
import datetime

class ResponseGif(ResponseCooldown):

    message = "#gif"

    RESPONSE_KEY = "#gif"

    COOLDOWN = 1 * 60 * 60 * 3 / 2

    url = 'http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag={term}'
    url_9to5 = 'http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag={term}&rating=pg'

    def __init__(self, msg, sender):
        super(ResponseGif, self).__init__(msg, sender, self.__module__, ResponseGif.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            out = ""
            search_term = self.msg.partition(' ')[2]
            if "spider" in search_term:
                return "fuck spiders, fuck you"
            hour = datetime.datetime.utcnow().hour
            is_weekday = datetime.datetime.utcnow().weekday() < 5
            EST_9AM = 8 + 5 # 0 indexed hours (9 AM = 8), and 5 hour UTC offset
            EST_5PM = 4 + 12 + 5
            is_during_workday = EST_9AM < hour < EST_5PM
            print("hour is: {}".format(hour))
            print("is it a weekday? {}".format(is_weekday))
            url_to_format = ResponseGif.url
            if (is_weekday and is_during_workday):
                print("PG-ifying the gif response")
                url_to_format = ResponseGif.url_9to5

            request_url = url_to_format.format(term=search_term)
            response = requests.get(request_url)
            try:
                print request_url
                out = response.json()["data"]["image_url"]
            except Exception:
                out = "Something went wrong"

            return out
        else:
            print("not responding to gif because sender {} is on cooldown".format(self.sender))
