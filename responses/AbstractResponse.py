import json
import os
import traceback

import pymongo
import time
import sys
import difflib

from data import DataAccess
from utils import output_message


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
        try:
            response = self._respond()
            return response
        except:
            exception_string = traceback.format_exc()
            self.add_to_response_storage_list('exceptions', exception_string, 10)
            return response

    def _respond(self):
        return None

    def add_to_response_storage_list(self, key, value, limit=None):
        if not self.clazzname:
            return None
        stored_list = self.get_response_storage(key)
        if not stored_list:
            stored_list = []
        stored_list.append(value)
        if limit:
            stored_list = stored_list[(-1 * limit):]
        self.set_response_storage(key, stored_list)

    def get_response_storage(self, key, other_class = None):
        if not self.clazzname:
            return None
        if other_class == None:
            ref = self.clazzname
        else:
            ref = other_class
        da = DataAccess.DataAccess()
        return da.get_response_storage(ref, key)

    def set_response_storage(self, key, value, other_class = None):
        if not self.clazzname:
            return None
        if other_class == None:
            ref = self.clazzname
        else:
            ref = other_class
        da = DataAccess.DataAccess()
        da.set_response_storage(ref, key, value)

    @classmethod
    def is_relevant_msg(cls, msg):
        return cls.RESPONSE_KEY in msg.text.lower()
