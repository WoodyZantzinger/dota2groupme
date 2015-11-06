# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
import datetime


class ResponseGetAJob(AbstractResponse):

    OVERRIDE_PRIORITY = 4

    EST_UTC_OFFSET = 5

    def __init__(self, msg):
        super(ResponseGetAJob, self).__init__(msg)

    def respond(self):
        return "Get a job"

    @classmethod
    def is_relevant_msg(cls, msg):
        hour = datetime.datetime.utcnow().hour
        is_weekday = datetime.datetime.utcnow().weekday() <= 5
        EST_9AM = 8 + 5  # 0 indexed hours (9 AM = 8), and 5 hour UTC offset
        EST_5PM = 4 + 12 + 5
        is_during_workday = EST_9AM < hour < EST_5PM
        return is_during_workday and "games" in msg.text and is_weekday and "?" in msg.text



