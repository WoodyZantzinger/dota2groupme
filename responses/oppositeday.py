# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*
from .AbstractResponse import AbstractResponse


class ResponseOppositeDay(AbstractResponse):

    RESPONSE_KEY = "#oppositeday"

    opposite_mode_enabled = False

    def __init__(self, msg):
        super(ResponseOppositeDay, self).__init__(msg)

    def respond(self):
        if ResponseOppositeDay.opposite_mode_enabled:
            ResponseOppositeDay.opposite_mode_enabled = False
            return "It is no longer opposite day"
        else:
            ResponseOppositeDay.opposite_mode_enabled = True
            return "It is now opposite day"

