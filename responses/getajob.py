# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
import datetime



class ResponseGetAJob(AbstractResponse):

    OVERRIDE_PRIORITY = 4

    def __init__(self, msg, sender):
        super(ResponseGetAJob, self).__init__(msg, sender)

    def respond(self):
        return "Get a job"

    @classmethod
    def is_relevant_msg(cls, msg, sender):
        hour = datetime.datetime.now().hour
        isweekday = datetime.datetime.now().weekday() <= 5
        return 9 < hour < 17 and "games" in msg and isweekday



