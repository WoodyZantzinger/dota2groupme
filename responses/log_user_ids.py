# -*- coding: utf-8 -*
import logging
import traceback

from .CooldownResponse import *
import re


class ResponseLogUserIDs(ResponseCooldown):
    COOLDOWN = 60 * 60 * 12
    SEARCH_STRING = ".*Wordle\s\d+\s\d/\d.*"
    LOG_KEY_NAME = "UserIDLog"

    def __init__(self, msg):
        super(ResponseLogUserIDs, self).__init__(msg, self, ResponseLogUserIDs.COOLDOWN)

    def _respond(self):
        try:
            local_id = str(self.msg.user_id)
            service = self.msg.from_service
            name = self.msg.name

            results_log = self.get_response_storage(ResponseLogUserIDs.LOG_KEY_NAME)
            results_log = results_log or dict()
            if service not in results_log:
                print("adding new user to results log")
                results_log[service] = {}
            results_log[service][local_id] = name
            self.set_response_storage(ResponseLogUserIDs.LOG_KEY_NAME, results_log)
        except Exception as e:
            print("In RLUIDs: " + str(e))
        return None


    @classmethod
    def is_relevant_msg(cls, msg):
        print("\t USER ID LOG > " + msg.text)
        print("\t USER ID LOG > " + str(msg.sender_id))
        print("\t USER ID LOG > " + str(msg.user_id))

        return True
