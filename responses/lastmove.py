# -*- coding: utf-8 -*
from .AbstractResponse import *
from .CooldownResponse import *
import requests
from responses import oAuth_util
import dateutil.parser


class last_move(AbstractResponse):

    message = "#move"

    RESPONSE_KEY = "#move"

    COOLDOWN = 1 * 60 * 60 * 3 / 2

    url = "https://www.strava.com/api/v3/activities?access_token={token}"

    def __init__(self, msg):
        super(last_move, self).__init__(msg)

    def respond(self):
        conn = pymongo.MongoClient(oAuth_util.get_db_url())
        SpotifyUsers = conn.dota2bot.spotify
        temp = SpotifyUsers.find_one({'GroupmeID': self.msg.sender_id})
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
            URL = ("You need to Auth\nhttps://www.strava.com/oauth/authorize?"
            "client_id=7477"
            "&response_type=code"
            "&redirect_uri=https://young-fortress-3393.herokuapp.com/strava_token"
            "&scope=view_private"
            "&state=" + self.msg.sender_id +
            "&approval_prompt=force"
            )
            return URL
