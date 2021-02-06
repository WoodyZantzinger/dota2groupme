# -*- coding: utf-8 -*
from .AbstractResponse import *
from .CooldownResponse import *
import random

users = DataAccess.DataAccess().get_users()
people = [user.values['Name'] for user in users]


class ResponseWho(ResponseCooldown):
    RESPONSE_KEY = "#who"

    COOLDOWN = 1 * 60 * 60 / 4

    def __init__(self, msg):
        super(ResponseWho, self).__init__(msg, self, ResponseWho.COOLDOWN)

    def _respond(self):
        if "two thumbs" in self.msg.text:
            out = "^^ this guy"
        elif "gonna call" in self.msg.text:
            out = "Ghostbusters!"
        else:
            out = random.choice(list(people))
        return out
