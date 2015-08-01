# -*- coding: utf-8 -*
from AbstractResponse import *
from CooldownResponse import *
import requests
import datetime
import auth_strava
import dateutil.parser

class last_move(ResponseCooldown):

    message = "#move"

    RESPONSE_KEY = "#move"

    COOLDOWN = 1 * 60 * 60 * 3 / 2

    url = "https://www.strava.com/api/v3/activities?access_token={token}"

    def __init__(self, msg):
        super(last_move, self).__init__(msg, self.__module__, last_move.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            conn = pymongo.Connection(auth_strava.get_db_url())
            StravaUsers = conn.dota2bot.strava
            temp = StravaUsers.find_one({'GroupmeID': self.msg.sender_id})
            if temp is not None:
                Token = temp["access_token"]
                request_url = last_move.url.format(token=Token)
                response = requests.get(request_url)
                try:
                    print request_url
                    miles = response.json()[0]["distance"] / 1609.34
                    time = response.json()[0]["elapsed_time"] / 60 / miles
                    location = response.json()[0]["location_city"]
                    type = response.json()[0]["type"]
                    date = dateutil.parser.parse(response.json()[0]["start_date_local"]).date()
                    out = str(date) + ": You went " + "{0:.2f}".format(miles) + " miles at a " + "{0:.2f}".format(time) + "minute/mile pace in " + location + " (" + type + ")"
                except Exception as e:
                    out = "Something went wrong: " + str(e)
                self.note_response(out)
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
        else:
            print("not responding to gif because sender {} is on cooldown".format(self.sender))
