# -*- coding: utf-8 -*
import logging
import traceback

from .CooldownResponse import *
import re


class ResponseWordle(ResponseCooldown):
    COOLDOWN = 60 * 60 * 12
    SEARCH_STRING = ".*Wordle\s\d+\s\d/\d.*"
    LOG_KEY_NAME = "wordle_results_log"

    def __init__(self, msg):
        super(ResponseWordle, self).__init__(msg, self, ResponseWordle.COOLDOWN)

    def _respond(self):
        try:
            found = re.search(ResponseWordle.SEARCH_STRING, self.msg.text)
            success_line = self.msg.text[found.span()[0]:found.span()[1]]

            parts = success_line.strip().split()
            game_number = parts[1]
            guesses = parts[2]
            n_guesses = guesses.split('/')[0]
            success = int(n_guesses) in [1, 2, 3, 4, 5, 6]
            if success:
                sender_id = self.msg.sender_id
                results_log = self.get_response_storage(ResponseWordle.LOG_KEY_NAME)
                results_log = results_log or dict()
                if sender_id not in results_log:
                    print("adding new user to results log")
                    results_log[sender_id] = {}
                results_log[sender_id][game_number] = str(n_guesses)
                self.set_response_storage(ResponseWordle.LOG_KEY_NAME, results_log)
        except Exception as ex:
            print(ex)


    @classmethod
    def is_relevant_msg(cls, msg):
        if re.search(ResponseWordle.SEARCH_STRING, msg.text):
            return True
        return False
