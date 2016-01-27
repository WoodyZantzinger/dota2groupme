# -*- coding: utf-8 -*
from CooldownResponse import *


class ResponseSpecificGif(ResponseCooldown):

    COOLDOWN = 1 * 60 * 60

    GIF_MAP = { "letsgoalready" : "http://media.giphy.com/media/y4HyxvrP8JRhm/giphy.gif",
                "neat" : "http://i.imgur.com/zCBQP8s.gif",
                "imaprick" : "http://media.giphy.com/media/ueUKby1TWZPpe/giphy.gif",
                 "iwanttogo": "http://media.giphy.com/media/xMFawXGPvt05y/giphy.gif",
                 "wheresthepizza": "http://media.giphy.com/media/qwvi00BCm6OmQ/giphy.gif",
                 "rememberme": "http://mrwgifs.com/wp-content/uploads/2013/08/Remember-Me-Bender-The-Great-Pharaoh-On-Futurama.gif",
                 "haters": "http://i.imgur.com/75dta.gif",
                 "datass": "http://26.media.tumblr.com/tumblr_lw7lvvZz9n1r5zq6ao1_500.gif",
                 "aliens": "http://i0.kym-cdn.com/photos/images/original/000/155/594/yesitis2.gif?1311943181",
                 "pooping": "http://media.tumblr.com/tumblr_m0t0ykVDMu1qzozj1.gif",
                 "tearsofunfathomablesadness": "http://i.imgur.com/X3TeVee.gif",
                 "whatatimetobealive": "http://i.imgur.com/gKBQ0cg.gif",
                 "disappointed": "http://i.imgur.com/AAaiGlu.gif"
                 }

    def __init__(self, msg):
        super(ResponseSpecificGif, self).__init__(msg, self.__module__, ResponseSpecificGif.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            out = None
            for word in self.msg.text.split(" "):
                if word.startswith("#") and word[1:] in ResponseSpecificGif.GIF_MAP:
                    out = ResponseSpecificGif.GIF_MAP[word[1:]]
            self.note_response(out)
            return out
        else:
            print("not responding to gif because sender {} is on cooldown".format(self.msg.name))

    @classmethod
    def is_relevant_msg(cls, msg):
        for word in msg.text.split(" "):
            if word.startswith("#") and word[1:] in ResponseSpecificGif.GIF_MAP:
                return True

