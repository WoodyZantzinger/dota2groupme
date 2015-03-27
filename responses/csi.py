# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
import random


class ResponseCSI(AbstractResponse):

    RESPONSE_KEY = "#csi"

    HELP_RESPONSE = "Sends a yeahhhh response"

    yeahhh_responses = ["http://giphy.com/gifs/csi-miami-explosion-david-caruso-PcTzEWBzqiL5u",
"http://giphy.com/gifs/shades-csi-miami-szRuBQwXkSsXm",
"http://giphy.com/gifs/deal-with-it-godzilla-d0SEajOmMna1i",
"http://giphy.com/gifs/funny-hilarious-deal-with-it-IQjbS7v9eYivm",
"http://giphy.com/gifs/dealwithit-rseRYN6UZCDUQ",
"http://giphy.com/gifs/deal-with-it-pokemon-meme-53qvTOxCBGTf2",
"http://giphy.com/gifs/deal-with-it-bra-frustration-oe8Bzgk1FaMSc",
"http://giphy.com/gifs/deal-with-it-regular-show-1089GpdYOAvZHq",
"http://giphy.com/gifs/deal-with-it-oprah-B7bLPuQgCJRKg",
"http://giphy.com/gifs/deal-with-it-dance-askreddit-f6pOe5e8ShRhS",
"http://giphy.com/gifs/deal-with-it-sunglasses-jack-nicholson-Nx2Lx1RmLadtC",
"http://i.imgur.com/oEe6BBr.jpg"

                        ]

    def __init__(self, msg, sender):
        super(ResponseCSI, self).__init__(msg, sender)

    def respond(self):
        return random.choice(ResponseCSI.yeahhh_responses)