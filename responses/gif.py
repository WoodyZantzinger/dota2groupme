# -*- coding: utf-8 -*
import random
import re
from urllib import parse, request

from .AbstractResponse import *
from .CooldownResponse import *
import requests
import datetime
import urllib
from random import randrange
from azure.cognitiveservices.search.imagesearch import ImageSearchClient
from msrest.authentication import CognitiveServicesCredentials
from utils import output_message
import urllib.request
from enum import Enum
import random

class GifService(Enum):
    GIPHY = 1
    AZURE = 2

SERVICE_TO_USE = GifService.GIPHY

class ResponseGif(ResponseCooldown):

    message = "#gif"

    RESPONSE_KEY = "#gif"

    COOLDOWN = 1 * 60 * 60 * 3 / 2

    url = "https://api.giphy.com/v1/gifs/search"

    def __init__(self, msg):
        super(ResponseGif, self).__init__(msg, self, ResponseGif.COOLDOWN)

    def _respond(self):
        azure_key = DataAccess.get_secrets()['AZURE_KEY']
        giphy_key = DataAccess.get_secrets()['GIPHY_KEY']

        out = ""
        search_term = self.msg.text.partition(' ')[2].lower()
        req_term = self.msg.text.partition(' ')[0].lower()
        if "spider" in search_term:
            return "fuck spiders, fuck you"
        while search_term.find(".com") + search_term.find(".net") + search_term.find(".porn") > 0:
            search_term = search_term.replace(".com", "")
            search_term = search_term.replace(".net", "")
            search_term = search_term.replace(".porn", "")

        search_term = self.remove_banned_words(search_term)

        hour = datetime.datetime.utcnow().hour
        # 0 == MONDAY for weekday()
        is_weekday = 0 <= datetime.datetime.utcnow().weekday() <= 4
        EST_9AM = 6 + 5  # 0 indexed hours (9 AM = 8), and 5 hour UTC offset
        EST_5PM = 7 + 12 + 5
        is_during_workday = EST_9AM < hour < EST_5PM
        # print("hour is: {}".format(hour))
        # print("is it a weekday? {}".format(is_weekday))

        rating = "pg"
        if (is_weekday and is_during_workday):
            print("PG-ifying the gif response")
            rating = "g"

        if SERVICE_TO_USE == GifService.GIPHY:
            #use Giphy
            params = parse.urlencode({
                "api_key": giphy_key,
                "rating": rating,
                "q": search_term,
                "limit":50
            })


            try:
                response = requests.get(url)
                data = response.json()

                if response.status_code == 200 and data["data"]:
                    chosen_gif = random.choice(data["data"])
                    gif_url = chosen_gif["images"]["original"]["url"]
                    return output_message.OutputMessage(gif_url, output_message.Services.PHOTO_URL)                    
            except Exception as e:
                raise e

        if SERVICE_TO_USE == GifService.AZURE:
            #use Azure
            search_term = search_term.encode("utf-8")
            client = ImageSearchClient(endpoint="https://api.cognitive.microsoft.com", credentials=CognitiveServicesCredentials(azure_key))
            image_results = client.images.search(query=search_term, safe_search="Strict", image_type="AnimatedGif")

            if image_results.value:
                out = ""
                image_results.value = self.remove_banned_websites(image_results.value)
                while(out == ""):
                    max = 1
                    if req_term == "#gif":
                        max = min(len(image_results.value), 50)
                    if req_term == "#gifone":
                        max = 1
                    first_image_result = image_results.value[randrange(max)]
                    image_url = first_image_result.content_url
                    return output_message.OutputMessage(image_url, output_message.Services.PHOTO_URL)
                    # out = HostImage(first_image_result.content_url)
            else:
                out = "Found nothing"
        return out

    def remove_banned_words(self, search_term):
        # print(f"Original search term = {search_term}")
        banned_words = self.get_response_storage('banned_words')
        # print(banned_words)
        if banned_words:
            things = None
            with open(os.path.join("utils", "things.txt")) as f:
                things = [line.rstrip('\n') for line in f]
            for bad_word in banned_words:
                search_term = re.sub(bad_word, random.choice(things), search_term)
        # print(f"Modified search term = {search_term}")
        return search_term

    def remove_banned_websites(self, image_results):
        banned_sites = self.get_response_storage('banned_sites')
        results = []
        if banned_sites:
            for result in image_results:
                if not any([site in result.content_url for site in banned_sites]):
                    results.append(result)
        else:
            results = image_results
        return results
