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

    url = "https://api.spotify.com/v1/me/player/currently-playing"

    def __init__(self, msg):
        super(nowmusic, self).__init__(msg)

    def respond(self):
        conn = pymongo.MongoClient(oAuth_util.get_db_url())
        SpotifyUsers = conn.dota2bot.spotify
        temp = SpotifyUsers.find_one({'GroupmeID': self.msg.sender_id})
        if temp is not None:
            Token = temp["access_token"]
            headers = {'Authorization': 'Bearer ' + str(Token)}
            try:
                response = requests.get(nowmusic.url, headers=headers)
                currently_playing = response.json()["is_playing"]
                song = response.json()["item"]["name"]
                artist = response.json()["item"]["artists"][0]["name"]
                if currently_playing:
                    out = "Currently listening to " + song + " by " + artist
                else:
                    out = "Last listened to " + song + " by " + artist
            except Exception as e:
                out = "Something went wrong: " + str(e)
            return out
        else:
            URL = ("You need to Auth\nhhttps://accounts.spotify.com/authorize?"
            "client_id=f8597c3f9afb4c1f9f0d3e8d5b53d4ae"
            "&response_type=code"
            "&redirect_uri=https://young-fortress-3393.herokuapp.com/spotify_callback"
            "&scope=user-read-currently-playing user-read-playback-state"
            "&state=" + self.msg.sender_id
            )
            return URL
