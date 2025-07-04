# -*- coding: utf-8 -*
from .AbstractResponse import AbstractResponse
from utils.emulate.emulate import *
from utils import BaseMessage
import random


class chitchat(AbstractResponse):

    RESPOND_THRESHOLD = 0.01

    OVERRIDE_PRIORITY = 5

    ENABLED = False

    def __init__(self, msg):
        super(chitchat, self).__init__(msg)

    def _respond(self):
        message = self.msg.text
        return generate_response(message, 0)

    @classmethod
    def is_relevant_msg(cls, msg: BaseMessage):
        could_be_url = "http" in msg.text or "www" in msg.text or ".com" in msg.text
        not_self = msg.get_sender_uid() != AbstractResponse.GroupMeIDs["sUN"]
        booleans = not could_be_url and not_self
        #return random.random() < chitchat.RESPOND_THRESHOLD and booleans

