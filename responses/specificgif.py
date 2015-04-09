# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseSpecificGif(AbstractResponse):

    GIF_MAP = { "letsgoalready" : "http://media.giphy.com/media/y4HyxvrP8JRhm/giphy.gif",
                "neat" : "http://i.imgur.com/zCBQP8s.gif",
                "imaprick" : "http://media.giphy.com/media/ueUKby1TWZPpe/giphy.gif",
                 "iwanttogo": "http://media.giphy.com/media/xMFawXGPvt05y/giphy.gif",
                 "wheresthepizza": "http://media.giphy.com/media/qwvi00BCm6OmQ/giphy.gif"
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

