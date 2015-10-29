# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
from nexthero import ResponseNext

class ResponseNextTeam(AbstractResponse):

    RESPONSE_KEY = "#nextteam"

    HELP_RESPONSE = "The next awesome team to draft"

    team_template = "The best team ever: {}, {}, {}, {}, {}"

    def __init__(self, msg, sender):
        super(ResponseNextTeam, self).__init__(msg, sender)

    def respond(self):
        heroes = [ResponseNext.random_hero() for _ in range(5)]
        return ResponseNextTeam.team_template.format(*heroes)