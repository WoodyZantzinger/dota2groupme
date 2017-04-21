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
            headers = {'Authorization': 'Bearer ' + str(temp["access_token"])}
            try:
                response = requests.get(nowmusic.url, headers=headers)
                if (response.status_code == 401):
                    r = requests.post('https://accounts.spotify.com/api/token', data = {
                        'grant_type':'authorization_code',
                        'client_id':'f8597c3f9afb4c1f9f0d3e8d5b53d4ae',
                        'redirect_uri':'https://young-fortress-3393.herokuapp.com/spotify_callback',
                        'client_secret': oAuth_util.get_spotify_key(),
                        'code': temp["refresh_token"]})


                    SpotifyData = r.json()
                    temp["access_token"] = SpotifyData["access_token"]
                    temp["refresh_token"] = SpotifyData["refresh_token"]

                    SpotifyUsers.update({'_id': temp["_id"]}, {"$set": temp}, upsert=True)

                    #Try again
                    headers = {'Authorization': 'Bearer ' + str(temp["access_token"])}
                    response = requests.get(nowmusic.url, headers=headers)
                elif (response.status_code == 200):
                    currently_playing = response.json()["is_playing"]
                    song = response.json()["item"]["name"]
                    artist = response.json()["item"]["artists"][0]["name"]
                    if currently_playing:
                        out = "Currently listening to " + song + " by " + artist
                    else:
                        out = "Last listened to " + song + " by " + artist
                else:
                    out = "Something went wrong: HTTP status != 200 or 401 (blame Mike)"

            except Exception as e:
                out = "Something went wrong: " + str(e)
            return out
        else:
            URL = ("You need to Auth\nhhttps://accounts.spotify.com/authorize?"
            "client_id=f8597c3f9afb4c1f9f0d3e8d5b53d4ae"
            "&response_type=code"
            "&redirect_uri=https://young-fortress-3393.herokuapp.com/spotify_callback"
            "&scope=user-read-currently-playing%20user-read-playback-state"
            "&state=" + self.msg.sender_id
            )
            return URL
