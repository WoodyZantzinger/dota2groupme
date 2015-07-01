# -*- coding: utf-8 -*
from AbstractResponse import *
import sys
import time
from utils import cachedmessage


class ResponseCooldown(AbstractResponse):

    def __init__(self, msg, sender, mod, cooldown):
        super(ResponseCooldown, self).__init__(msg, sender, mod)
        self.cooldown = cooldown
        self.mod = mod
        if not hasattr(sys.modules[mod], 'last_used'):
            setattr(sys.modules[mod], 'last_used', dict())
            getattr(sys.modules[mod], 'last_used')[sender] = []
        else:
            if not sender in getattr(sys.modules[mod], 'last_used'):
                getattr(sys.modules[mod], 'last_used')[sender] = []

    def is_sender_off_cooldown(self):
        can_send = False
        messages = getattr(sys.modules[self.mod], 'last_used')[self.sender]
        if not len(messages):
            can_send = True
        else:
            last_msg = messages[-1]
            elapsed_time = time.time() - last_msg.time
            print("elapsed time is {}, and cooldown is {}".format(elapsed_time, self.cooldown))
            if elapsed_time > self.cooldown:
                can_send = True
        if can_send:
            getattr(sys.modules[self.mod], 'last_used')[self.sender].append(cachedmessage.CachedMessage(self.msg))
        return can_send

    def note_response(self, response):
        getattr(sys.modules[self.mod], 'last_used')[self.sender][-1].response = response
        self.print_responses()

    def print_responses(self):
        print("past messages are:")
        for _ in getattr(sys.modules[self.mod], 'last_used')[self.sender]:
            print(_)

    def respond(self):
        pass
