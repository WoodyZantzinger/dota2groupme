# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseSpecificGif(AbstractResponse):

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
                 }

    def __init__(self, msg, sender):
        super(ResponseSpecificGif, self).__init__(msg, sender)

    def respond(self):
        for word in self.msg.split(" "):
            if word.startswith("#") and word[1:] in ResponseSpecificGif.GIF_MAP:
                return ResponseSpecificGif.GIF_MAP[word[1:]]

    @classmethod
    def is_relevant_msg(cls, msg, sender):
        for word in msg.split(" "):
            if word.startswith("#") and word[1:] in ResponseSpecificGif.GIF_MAP:
                return True

