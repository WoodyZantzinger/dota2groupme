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
        if ("#gif" in self.msg):
            return "<a href=\"{}\">{}</a> : <br> <img src=\"{}\">".format(self.response, self.msg, self.response)
        return "<a href=\"{}\">{}</a> : {}".format(self.response, self.msg, self.response)
