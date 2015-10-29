# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse


class ResponseGroupMeNameUpdate(AbstractResponse):

    CHANGE_STR = " changed name to "

    def __init__(self, msg, sender):
        super(ResponseGroupMeNameUpdate, self).__init__(msg, sender)

    def respond(self):
        old, new = self.msg.split(ResponseGroupMeNameUpdate.CHANGE_STR)
        AbstractResponse.update_user(old, new)

    @classmethod
    def is_relevant_msg(cls, msg, sender):
        #@TODO notice if sender is admin or regular user
        from_user = False
        for person in AbstractResponse.GroupMetoSteam:
            if sender == person:
                from_user = True
        return ResponseGroupMeNameUpdate.CHANGE_STR in msg and not from_user
