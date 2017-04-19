__author__ = 'woodyzantzinger'
# -*- coding: utf-8 -*
from AbstractResponse import *
from CooldownResponse import *
import requests
import oAuth_util
import dateutil.parser


class nowmusic(AbstractResponse):

    message = "#music"

    RESPONSE_KEY = "#music"

    COOLDOWN = 1 * 60 * 60 * 3 / 2

    url = "TODO"

    def __init__(self, msg):
        super(nowmusic, self).__init__(msg)

    def respond(self):
        conn = pymongo.MongoClient(oAuth_util.get_db_url())
        StravaUsers = conn.dota2bot.strava
        temp = StravaUsers.find_one({'GroupmeID': self.msg.sender_id})
        if temp is not None:
            Token = temp["access_token"]
            request_url = last_move.url.format(token=Token)
            response = requests.get(request_url)
            try:
                print(request_url)
                miles = response.json()[0]["distance"] / 1609.34
                time = response.json()[0]["elapsed_time"] / 60 / miles
                location = response.json()[0]["location_city"]
                move_type = response.json()[0]["type"]
                date = dateutil.parser.parse(response.json()[0]["start_date_local"]).date()
                out = str(date) + ": You went " + "{0:.2f}".format(miles) + " miles at a " + "{0:.2f}".format(time) + "minute/mile pace in " + location + " (" + move_type + ")"
            except Exception as e:
                out = "Something went wrong: " + str(e)
            return out
        else:
            URL = ("You need to Auth\nhhttps://accounts.spotify.com/authorize?"
            "client_id=f8597c3f9afb4c1f9f0d3e8d5b53d4ae"
            "&response_type=code"
            "&redirect_uri=https://young-fortress-3393.herokuapp.com/spotify_callback"
            "&state=" + self.msg.sender_id
            )
            return URL
