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
    DATA_ACCESS_URL = r"https://api.spotify.com/v1/me/player/currently-playing"
    REQUEST_SCOPES = [
        "user-read-currently-playing",
        "user-read-playback-state"
    ]

    message = "#music"

    RESPONSE_KEY = "#music"

    COOLDOWN = 1 * 60 * 60 * 3 / 2

    url = "https://api.spotify.com/v1/me/player/currently-playing"

    def __init__(self, msg):
        self.response = None
        super(Spotify_Last, self).__init__(msg, self)

    def respond(self):
        # should already have data???
        if self.outcome.data:
            data = self.outcome.data
            currently_playing = data["is_playing"]
            song = data["item"]["name"]
            artist = data["item"]["artists"][0]["name"]
            if currently_playing:
                out = "Currently listening to " + song + " by " + artist
            else:
                out = "Last listened to " + song + " by " + artist
            self.response = out
        super(Spotify_Last, self).respond()
        return self.response