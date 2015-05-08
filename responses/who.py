# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
import random


class ResponseWho(AbstractResponse):

    RESPONSE_KEY = "#who"

    def __init__(self, msg, sender):
        super(ResponseWho, self).__init__(msg, sender)

    def respond(self):
        people = []
        for person, steamid in AbstractResponse.GroupMetoSteam.iteritems():
            people.append(person)
        return random.choice(people)

