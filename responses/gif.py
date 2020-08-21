# -*- coding: utf-8 -*
from .AbstractResponse import *
from .CooldownResponse import *
import requests
import datetime
import urllib
from random import randrange
from azure.cognitiveservices.search.imagesearch import ImageSearchClient
from msrest.authentication import CognitiveServicesCredentials
import urllib.request

def HostImage(url):
    GM_key = None
    try:
        with open('local_variables.json') as f:
            local_var = json.load(f)
            GM_key = local_var["GROUPME_AUTH"]
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        GM_key = os.getenv('GROUPME_AUTH')

    r = requests.get(url)
    url = 'https://image.groupme.com/pictures'

    header = {'X-Access-Token': GM_key, 'Content-Type': 'image/gif'}
    try:
        req = urllib.request.Request(url, r.content, header)
        response = urllib.request.urlopen(req)
        JSON_response = json.load(response)
        return (JSON_response["payload"]["picture_url"])
    except urllib.error.HTTPError:
        print("There was some sort of error uploading the photo")
        print(r.content)
        return ""


class ResponseGif(ResponseCooldown):

    message = "#gif"

    RESPONSE_KEY = "#gif"

    COOLDOWN = 1 * 60 * 60 * 3 / 2

    url = 'http://api.giphy.com/v1/gifs/random?api_key={key}&tag={term}&rating=pg'
    url_9to5 = 'http://api.giphy.com/v1/gifs/random?api_key={key}&tag={term}&rating=g'

    def __init__(self, msg):
        super(ResponseGif, self).__init__(msg, self.__module__, ResponseGif.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():

            azure_key = None
            try:
                with open('local_variables.json') as f:
                    local_var = json.load(f)
                    azure_key = local_var["AZURE_KEY"]
            except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
                azure_key = os.getenv('AZURE_KEY')

            key = None
            try:
                with open('local_variables.json') as f:
                    local_var = json.load(f)
                    key = local_var["GIPHY_KEY"]
            except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
                key = os.getenv('GIPHY_KEY')

            out = ""
            search_term = self.msg.text.partition(' ')[2].lower()
            req_term = self.msg.text.partition(' ')[0].lower()
            if "spider" in search_term:
                return "fuck spiders, fuck you"
            while search_term.find(".com") + search_term.find(".net") + search_term.find(".porn") > 0:
                search_term = search_term.replace(".com", "")
                search_term = search_term.replace(".net", "")
                search_term = search_term.replace(".porn", "")
#            if "ariana" in search_term and "grande" in search_term:
#		return "her?"
            hour = datetime.datetime.utcnow().hour
            # 0 == MONDAY for weekday()
            is_weekday = 0 <= datetime.datetime.utcnow().weekday() <= 4
            EST_9AM = 6 + 5  # 0 indexed hours (9 AM = 8), and 5 hour UTC offset
            EST_5PM = 7 + 12 + 5
            is_during_workday = EST_9AM < hour < EST_5PM
            print("hour is: {}".format(hour))
            print("is it a weekday? {}".format(is_weekday))
            url_to_format = ResponseGif.url
            if (is_weekday and is_during_workday):
                print("PG-ifying the gif response")
                url_to_format = ResponseGif.url_9to5

            if search_term == "":
                #use Giphy
                request_url = url_to_format.format(term=search_term, key=key)
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
                image_results = client.images.search(query=search_term, safe_search="Strict", image_type="AnimatedGif")

                if image_results.value:
                    out = ""
                    while(out == ""):
                        if req_term == "#gif": max = min(len(image_results.value), 50)
                        if req_term == "#gifone": max = 1
                        first_image_result = image_results.value[randrange(max)]
                        out = HostImage(first_image_result.content_url)
                else:
                    out = "Found nothing"

                self.note_response(out)
            return out
        else:
            print("not responding to gif because sender {} is on cooldown".format(self.msg.name.encode("utf-8")))
