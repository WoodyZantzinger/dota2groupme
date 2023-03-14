# -*- coding: utf-8 -*
from data.SSO_Manager import SSO_Outcome_Type
from .AbstractResponse import *
from .CooldownResponse import *
from .SSOResponse import *
import requests
from responses import oAuth_util, SSOResponse
import dateutil.parser
from data import SSO_Manager
import pprint


class Strava_Last(SSO_Response):

    AUTH_URL = r"https://www.strava.com/oauth/authorize"
    TOKEN_REFRESH_URL = r"https://www.strava.com/oauth/token"
    DATA_ACCESS_URL = r"https://www.strava.com/api/v3/activities"
    REQUEST_SCOPES = [
        "activity:read_all"
    ]

    message = "#move"

    RESPONSE_KEY = "#move"

    COOLDOWN = 1 * 60 * 60 * 3 / 2

    url = "https://www.strava.com/api/v3/activities?access_token={token}"

    def __init__(self, msg):

        self.response = None
        super(Strava_Last, self).__init__(msg, self)

    def _respond(self):
        # should already have data???
        try:
            if self.outcome.outcome_type == SSO_Outcome_Type.NO_TOKEN:
                return self.outcome.auth_url
        except:
            pass
        if self.outcome[0].data:
            data = self.outcome[0].data
            miles = data[0]["distance"] / 1609.34
            time = data[0]["elapsed_time"] / 60 / miles
            location = data[0]["location_city"]
            if not location:
                location = "<Unknown location>"
            move_type = data[0]["type"]
            date = dateutil.parser.parse(data[0]["start_date_local"]).date()
            self.response = str(date) + ": You went " + "{0:.2f}".format(miles) + " miles at a " + "{0:.2f}".format(time) + "minute/mile pace in " + location + " (" + move_type + ")"
        super(Strava_Last, self)._respond()
        return self.response