# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
import json
import os


def get_db_url():
    try:
        with open(os.path.join(os.path.dirname(__file__), '../local_variables.json')) as f:
            local_var = json.load(f)
        return local_var["MONGOLAB_URL"]
    except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
        return os.getenv('MONGOLAB_URL')
    except:
        return None


def get_strava_key():
    try:
        with open(os.path.join(os.path.dirname(__file__), '../local_variables.json')) as f:
            local_var = json.load(f)
        return local_var["STRAVA_KEY"]
    except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
        return os.getenv('STRAVA_KEY')
    except:
        return None

def get_spotify_key():
    try:
        with open(os.path.join(os.path.dirname(__file__), '../local_variables.json')) as f:
            local_var = json.load(f)
        return local_var["SPOTIFY_KEY"]
    except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
        return os.getenv('SPOTIFY_KEY')
    except:
        return None

class ResponseNow(AbstractResponse):

    RESPONSE_KEY = "#strava_auth"

    def __init__(self, msg):
        super(ResponseNow, self).__init__(msg)

    def respond(self):
        URL = ("https://www.strava.com/oauth/authorize?"
            "client_id= 7477"
            "&response_type=code"
            "&redirect_uri=http://localhost:5000/strava_token"
            "&scope=view_private"
            "&state=" + self.msg.sender_id +
            "&approval_prompt=force"
          )
        return URL

__author__ = 'woodyzantzinger'
