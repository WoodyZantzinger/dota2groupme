# -*- coding: utf-8 -*
from data import DataAccess
from .AbstractResponse import AbstractResponse


JON = DataAccess.DataAccess().get_user("GROUPME_ID", '898503')
class ResponseSausage(AbstractResponse):

    OVERRIDE_PRIORITY = 4

    def __init__(self, msg):
        super(ResponseSausage, self).__init__(msg)

    def _respond(self):
        return "But, {}, you don't even have any money".format(self.msg.name)

    @classmethod
    def is_relevant_msg(cls, msg):
        return JON['GROUPME_ID'] == msg.sender_id and 'sausage' in msg.text

