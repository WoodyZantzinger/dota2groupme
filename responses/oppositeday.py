# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
import steamapi


class ResponseOppositeDay(AbstractResponse):

    RESPONSE_KEY = "#oppositeday"

    opposite_mode_enabled = False

    def __init__(self, msg, sender):
        super(ResponseOppositeDay, self).__init__(msg, sender)

    def respond(self):
        if ResponseOppositeDay.opposite_mode_enabled:
            ResponseOppositeDay.opposite_mode_enabled = False
            return "It is no longer opposite day"
        else:
            ResponseOppositeDay.opposite_mode_enabled = True
            return "It is now opposite day"

