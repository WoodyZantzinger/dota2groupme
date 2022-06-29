# -*- coding: utf-8 -*
import random
import re

from .AbstractResponse import *
from .CooldownResponse import *
import requests
import datetime
import urllib
from random import randrange
from azure.cognitiveservices.search.imagesearch import ImageSearchClient
from msrest.authentication import CognitiveServicesCredentials
import urllib.request
from utils.GroupMeMessage import HostImage

class NoFilter(ResponseCooldown):

    message = "#nofilter"

    RESPONSE_KEY = "#nofilter"
    COST = 25
    COOLDOWN = 1


    url = 'http://api.giphy.com/v1/gifs/random?api_key={key}&tag={term}&rating=R'

    def __init__(self, msg):
        super(NoFilter, self).__init__(msg, self, NoFilter.COOLDOWN)

    #get_response_storage(self, "coins", "")

    def _respond(self):
        TOKEN_COUNT_KEY = "token_count"
        azure_key = DataAccess.get_secrets()['AZURE_KEY']
        giphy_key = DataAccess.get_secrets()['GIPHY_KEY']
        out = ""

        #can they spend?
        sender_id = self.msg.sender_id
        coin_storage = self.get_response_storage("coins", "ResponseSuperheart")

        if sender_id not in coin_storage or coin_storage[sender_id][TOKEN_COUNT_KEY] < NoFilter.COST:
            out = "You need " + str(NoFilter.COST) + " superhearts to do this"
        else:

            coin_storage[sender_id][TOKEN_COUNT_KEY] = coin_storage[sender_id][TOKEN_COUNT_KEY] - NoFilter.COST
            self.set_response_storage("coins", coin_storage, other_class="ResponseSuperheart")


            search_term = self.msg.text.partition(' ')[2].lower()
            req_term = self.msg.text.partition(' ')[0].lower()
            if "spider" in search_term:
                return "Still no spiders"

            url_to_format = NoFilter.url

            if search_term == "":
                #use Giphy
                request_url = url_to_format.format(term=search_term, key=giphy_key)
                response = requests.get(request_url)
                try:
                    print(request_url)
                    out = response.json()["data"]["image_url"]
                except Exception:
                    out = "Something went wrong"

            else:
                #use Azure
                search_term = search_term.encode("utf-8")
                client = ImageSearchClient(endpoint="https://api.cognitive.microsoft.com", credentials=CognitiveServicesCredentials(azure_key))
                image_results = client.images.search(query=search_term, safe_search="off", image_type="AnimatedGif")

                if image_results.value:
                    out = ""
                    #image_results.value = self.remove_banned_websites(image_results.value)
                    while(out == ""):
                        max = 1
                        if req_term == "#nofilter":
                            max = min(len(image_results.value), 50)
                        if req_term == "#nofiltertop":
                            max = 1
                        first_image_result = image_results.value[randrange(max)]
                        out = HostImage(first_image_result.content_url)
                else:
                    out = "Found nothing"
        return out