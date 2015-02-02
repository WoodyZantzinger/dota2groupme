# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
import datetime



class ResponseGetAJob(AbstractResponse):

    OVERRIDE_PRIORITY = 4

    EST_UTC_OFFSET = 5

    def __init__(self, msg, sender):
        super(ResponseGetAJob, self).__init__(msg, sender)

    def respond(self):
        return "Get a job"

    @classmethod
    def is_relevant_msg(cls, msg, sender):
        hour = datetime.datetime.utcnow().hour
        isweekday = datetime.datetime.utcnow().weekday() <= 5
        EST_9AM = 9 + ResponseGetAJob.EST_UTC_OFFSET
        EST_5PM = 17 + ResponseGetAJob.EST_UTC_OFFSET
        is_during_workday = EST_9AM < hour < EST_5PM
        return is_during_workday and "games" in msg and isweekday and "?" in msg



