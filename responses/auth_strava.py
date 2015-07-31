# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseNow(AbstractResponse):

    RESPONSE_KEY = "#strava_auth"

    def __init__(self, msg):
        super(ResponseNow, self).__init__(msg)

    def respond(self):
        URL = ("https://www.strava.com/oauth/authorize?"
            "client_id= 7477"
            "&response_type=code"
            "&redirect_uri=http://young-fortress-3393.herokuapp.com/strava_token"
            "&scope=view_private"
            "&state=" + self.msg.sender_id +
            "&approval_prompt=force"
          )
        return URL

__author__ = 'woodyzantzinger'
