# -*- coding: utf-8 -*
from .AbstractResponse import AbstractResponse
import random


class ResponseDeal(AbstractResponse):

    RESPONSE_KEY = "#deal"

    HELP_RESPONSE = "Sends a deal with it response"

    deal_responses = ["http://i.giphy.com/PcTzEWBzqiL5u.gif",
"http://i.giphy.com/d0SEajOmMna1i.gif",
"http://i.giphy.com/IQjbS7v9eYivm.gif",
"http://i.giphy.com/rseRYN6UZCDUQ.gif",
"http://i.giphy.com/53qvTOxCBGTf2.gif",
"http://i.giphy.com/oe8Bzgk1FaMSc.gif",
"http://i.giphy.com/1089GpdYOAvZHq.gif",
"http://i.giphy.com/B7bLPuQgCJRKg.gif",
"http://i.giphy.com/f6pOe5e8ShRhS.gif",
"http://i.giphy.com/Nx2Lx1RmLadtC.gif",
"http://i.imgur.com/oEe6BBr.jpg"]

    def __init__(self, msg):
        super(ResponseDeal, self).__init__(msg)

    def _respond(self):
        return random.choice(ResponseDeal.deal_responses)
