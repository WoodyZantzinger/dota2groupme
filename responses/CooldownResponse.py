# -*- coding: utf-8 -*
from AbstractResponse import *
import sys
import time
from utils import cachedmessage

USAGE_MEMBER_NAME = "usage_history"


class ResponseCooldown(AbstractResponse):

    def __init__(self, msg, mod, cooldown):
        super(ResponseCooldown, self).__init__(msg, mod)
        self.cooldown = cooldown
        self.mod = mod
        if not self.has_usage():
            self.set_usage(dict())
            self.get_usage()[self.msg.sender_id] = []
        else:
            if not self.msg.sender_id in self.get_usage():
                self.get_usage()[self.msg.sender_id] = []

    def is_sender_off_cooldown(self):
        can_send = False
        messages = self.get_usage()[self.msg.sender_id]
        if not len(messages):
            can_send = True
        else:
            last_msg = messages[-1]
            elapsed_time = time.time() - last_msg.time
            print("elapsed time is {}, and cooldown is {}".format(elapsed_time, self.cooldown))
            if elapsed_time > self.cooldown:
                can_send = True
        if can_send:
            self.get_usage()[self.msg.sender_id].append(cachedmessage.CachedMessage(self.msg.text))
        return can_send

    def note_response(self, response):
        print("noting a response for name of {} and id = {}".format(self.msg.name, self.msg.sender_id))
        self.get_usage()[self.msg.sender_id][-1].response = response
        #self.print_responses()

    def print_responses(self):
        print("past messages are:")
        for _ in self.get_usage()[self.msg.sender_id]:
            print(_)

    def get_usage(self):
        return getattr(sys.modules[self.mod], USAGE_MEMBER_NAME)

    def has_usage(self):
        return hasattr(sys.modules[self.mod], USAGE_MEMBER_NAME)

    def set_usage(self, obj):
        setattr(sys.modules[self.mod], USAGE_MEMBER_NAME, obj)

    def respond(self):
        pass
