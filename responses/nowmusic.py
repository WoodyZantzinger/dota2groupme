__author__ = 'woodyzantzinger'
# -*- coding: utf-8 -*
import urllib

from. AbstractResponse import *
from .CooldownResponse import *
from .SSOResponse import *
import requests
from responses import oAuth_util
import dateutil.parser


class Spotify_Last(SSO_Response):

    AUTH_URL = r"https://accounts.spotify.com/authorize"
    TOKEN_REFRESH_URL = r"https://accounts.spotify.com/api/token"
    DATA_ACCESS_URL = [r"https://api.spotify.com/v1/me/player/currently-playing",
                       r"https://api.spotify.com/v1/me/player/recently-played"]
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
        image_url = None
        song_url = None
        if self.outcome[0].data:
            data = self.outcome[0].data['item']
            song = data["name"]
            artist = data["artists"][0]["name"]
            out = "Currently listening to:\n" + song + " by " + artist
            # find album artwork URL and rehost
            # add rehosted URL to response
            image_url = data['album']['images'][1]['url']
            song_url = data['external_urls']['spotify']
            self.response = out
        elif self.outcome[1].data:
            data = self.outcome[1].data['items'][0]
            song = data["track"]["name"]
            artist = data["track"]["artists"][0]["name"]
            image_url = data["track"]["album"]["images"][1]['url']
            song_url = data["track"]['external_urls']['spotify']
            out = "Last listened to:\n" + song + " by " + artist
            # find album artwork URL and rehost
            # add rehosted URL to response
            self.response = out

        self.response = self.response + '\n' + song_url + '\n\U0001F3B6\n'
        super(Spotify_Last, self)._respond()
        return self.response