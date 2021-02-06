__author__ = 'woodyzantzinger'
# -*- coding: utf-8 -*
from. AbstractResponse import *
from .CooldownResponse import *
from .SSOResponse import *
import requests
from responses import oAuth_util
import dateutil.parser


class Spotify_Last(SSO_Response):

    AUTH_URL = r"https://accounts.spotify.com/authorize"
    TOKEN_REFRESH_URL = r"https://accounts.spotify.com/api/token"
    DATA_ACCESS_URL = r"https://api.spotify.com/v1/me/player/recently-played"
    REQUEST_SCOPES = [
        "user-read-currently-playing",
        "user-read-playback-state",
        "user-read-recently-played"
    ]

    message = "#music"

    RESPONSE_KEY = "#music"

    COOLDOWN = 1 * 60 * 60 * 3 / 2

    def __init__(self, msg):
        self.response = None
        super(Spotify_Last, self).__init__(msg, self)

    def _respond(self):
        # should already have data???
        if self.outcome.data:
            data = self.outcome.data['items'][0]
            song = data["track"]["name"]
            artist = data["track"]["artists"][0]["name"]
            out = "Last listened to " + song + " by " + artist
            self.response = out
        super(Spotify_Last, self)._respond()
        return self.response