# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
import random


class ResponseSunstrike(AbstractResponse):

    RESPONSE_KEY = "#sunstrike"

    HELP_RESPONSE = "Sends a random burn response"

    burn_responses = ["http://media.giphy.com/media/LOVjuAnxaUR6U/giphy.gif",
                      "http://media.giphy.com/media/jAugkVty2VCDu/giphy.gif",
                      "http://en.wikipedia.org/wiki/List_of_burn_centers_in_the_United_States",
                      "http://www.cabn.ca/en/canadian-burn-units-survivor-support-groups",
                      "https://38.media.tumblr.com/a86240b247fc8a3579fab663a61fec86/tumblr_mi1n1cm5a51rqfhi2o1_500.gif",
                      "http://spaghettiwithcrocetti.files.wordpress.com/2014/07/giphy-51.gif",
                      "http://i489.photobucket.com/albums/rr257/BBladem83/BurnNotice.gif",
                      "http://i.imgur.com/z7oi8te.gif",
                      "http://i.imgur.com/X991K.gif",
                      "http://i.imgur.com/Vz1mTb0.gif",
                      "http://i.imgur.com/nACY6nb.gif",
                      "http://i.imgur.com/WtDpHiL.gif",
                      "http://replygif.net/i/186.gif",
                      "http://i.imgur.com/HaoJTOE.gif",
                      "http://i.imgur.com/1obfI.gif",
                      "http://i.imgur.com/BWaY6.gif",
                      "http://i.imgur.com/pKqLWjo.gif"

                        ]

    def __init__(self, msg, sender):
        super(ResponseSunstrike, self).__init__(msg, sender)

    def respond(self):
        return random.choice(ResponseSunstrike.burn_responses)