# -*- coding: utf-8 -*
from CooldownResponse import *
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
        super(ResponseMagic8Ball, self).__init__(msg, self.__module__, ResponseMagic8Ball.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            out = random.choice(ResponseMagic8Ball.ANSWERS)
            self.note_response(out)
            return out
        print("not responding to yesorno because sender {} is on cooldown".format(self.msg.name))

