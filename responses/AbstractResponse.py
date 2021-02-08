import json
import os
import pymongo
import time
import sys
import difflib

from data import DataAccess


class AbstractResponse(object):
    # default response key
    # should respond to no messages
    RESPONSE_KEY = "\0"

    # priority of message overriding other messsages
    # to allow some things to make others not come through the pipe
    OVERRIDE_PRIORITY = 0

    ENABLED = True

    # default help response
    HELP_RESPONSE = "Not implemented for " + RESPONSE_KEY


    def __init__(self, msg, obj=None):
        super(AbstractResponse, self).__init__()
        if not obj:
            self.clazzname = None
        else:
            self.clazzname = obj.__class__.__name__
        self.msg = msg

    def respond(self):
        return self._respond()

    def _respond(self):
        return None

    def get_response_storage(self, key):
        if not self.clazzname:
            return None
        da = DataAccess.DataAccess()
        return da.get_response_storage(self.clazzname, key)

    def set_response_storage(self, key, value):
        if not self.clazzname:
            return None
        da = DataAccess.DataAccess()
        da.set_response_storage(self.clazzname, key, value)
    @classmethod
    def is_relevant_msg(cls, msg):
        return cls.RESPONSE_KEY in msg.text.lower()
