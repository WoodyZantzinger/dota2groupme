# -*- coding: utf-8 -*-
import time


class CachedMessage(object):

    def __init__(self, msg):
        super(CachedMessage, self).__init__()
        self.msg = msg
        self.time = time.time()
        self.response = None

    def __str__(self):
        return "<CachedMessage w/ m={}, t={}, r={}>".format(self.msg, self.time, self.response)

    def web_format(self):
        return "<a href=\"{}\">{}</a> : {}".format(self.response, self.msg, self.response)
