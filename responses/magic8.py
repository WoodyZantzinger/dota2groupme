# -*- coding: utf-8 -*
from .CooldownResponse import *
import random


class ResponseMagic8Ball(ResponseCooldown):

    RESPONSE_KEY = "#magic8"

    ANSWERS = ["It is certain",
                "It is decidedly so",
                "Without a doubt",
                "Yes definitely",
                "You may rely on it",
                "As I see it, yes",
                "Most likely",
                "Outlook good",
                "Yes",
                "Signs point to yes",
                "Reply hazy try again",
                "Ask again later",
                "Better not tell you now ;)",
                "Cannot predict now",
                "Concentrate and ask again",
                "Don't count on it",
                "My reply is no",
                "My sources say no",
                "Outlook not so good",
                "Very doubtful",
                "Maybe. Maybe not. Maybe fuck yourself"]

    COOLDOWN = 1 * 60 * 60 / 2

    def __init__(self, msg):
        super(ResponseMagic8Ball, self).__init__(msg, self, ResponseMagic8Ball.COOLDOWN)

    def _respond(self):
        out = random.choice(ResponseMagic8Ball.ANSWERS)
        return out

