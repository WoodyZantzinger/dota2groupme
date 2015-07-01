# -*- coding: utf-8 -*
from AbstractResponse import *
import sys
import time
from utils import cachedmessage

USAGE_MEMBER_NAME = "usage_history"


class ResponseCooldown(AbstractResponse):

    def __init__(self, msg, sender, mod, cooldown):
        super(ResponseCooldown, self).__init__(msg, sender, mod)
        self.cooldown = cooldown
        self.mod = mod
        if not self.has_usage():
            self.set_usage(dict())
            self.get_usage()[sender] = []
        else:
            if not sender in self.get_usage():
                self.get_usage()[sender] = []

    def is_sender_off_cooldown(self):
        can_send = False
        messages = self.get_usage()[self.sender]
        if not len(messages):
            can_send = True
        else:
            last_msg = messages[-1]
            elapsed_time = time.time() - last_msg.time
            print("elapsed time is {}, and cooldown is {}".format(elapsed_time, self.cooldown))
            if elapsed_time > self.cooldown:
                can_send = True
        if can_send:
            self.get_usage()[self.sender].append(cachedmessage.CachedMessage(self.msg))
        return can_send

    def note_response(self, response):
        self.get_usage()[self.sender][-1].response = response
        self.print_responses()

    def print_responses(self):
        print("past messages are:")
        for _ in self.get_usage()[self.sender]:
            print(_)

    def get_usage(self):
        return getattr(sys.modules[self.mod], USAGE_MEMBER_NAME)

    def has_usage(self):
        return hasattr(sys.modules[self.mod], USAGE_MEMBER_NAME)

    def set_usage(self, obj):
        setattr(sys.modules[self.mod], USAGE_MEMBER_NAME, obj)

    def respond(self):
        pass
