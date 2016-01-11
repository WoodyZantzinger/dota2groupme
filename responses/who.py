# -*- coding: utf-8 -*
from AbstractResponse import *
from CooldownResponse import *
import random


class ResponseWho(ResponseCooldown):

    RESPONSE_KEY = "#who"

    COOLDOWN = 1 * 60 * 60 / 4

    def __init__(self, msg):
        super(ResponseWho, self).__init__(msg, self.__module__, ResponseWho.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            people = set()
            out = None
            for person, steamid in AbstractResponse.GroupMetoSteam.iteritems():
                people.add(person)
            for person, xboxid in AbstractResponse.GroupMetoXbox.iteritems():
                people.add(person)
            if "two thumbs" in self.msg.text:
                out = "^^ this guy"
            elif "gonna call" in self.msg.text:
                out = "Ghostbusters!"
            else:
                out = random.choice(list(people))
            self.note_response(out)
            return out
        else:
            print("not responding to #who because sender {} is on cooldown".format(self.msg.name))
