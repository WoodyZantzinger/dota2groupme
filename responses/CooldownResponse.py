# -*- coding: utf-8 -*
from AbstractResponse import *
import sys
import time


class ResponseCooldown(AbstractResponse):

    def __init__(self, msg, sender, mod, cooldown):
        super(ResponseCooldown, self).__init__(msg, sender, mod)
        self.cooldown = cooldown
        self.mod = mod
        if not hasattr(sys.modules[mod], 'last_used'):
            setattr(sys.modules[mod], 'last_used', dict())
            getattr(sys.modules[mod], 'last_used')[sender] = 0
        else:
            if not sender in getattr(sys.modules[mod], 'last_used'):
                getattr(sys.modules[mod], 'last_used')[sender] = 0

    def is_sender_off_cooldown(self):
        last_time = getattr(sys.modules[self.mod], 'last_used')[self.sender]
        elapsed_time = time.time() - last_time
        print("elapsed time is {}, and cooldown is {}".format(elapsed_time, self.cooldown))
        if elapsed_time > self.cooldown:
            getattr(sys.modules[self.mod], 'last_used')[self.sender] = time.time()
            return True
        return False

    def respond(self):
        pass
