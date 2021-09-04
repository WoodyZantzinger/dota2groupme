# -*- coding: utf-8 -*
from utils import get_groupme_messages
from utils.rawmessage import RawMessage
from .AbstractResponse import *
import sys
import time

from .CooldownResponse import ResponseCooldown

class ResponseQuote(ResponseCooldown):
    usage = {}
    referenced_message = None
    group_id = None

    def __init__(self, msg):
        super(ResponseQuote, self).__init__(msg, self, 1)
        self.get_referenced_message()

    def get_referenced_message(self):
        if not hasattr(self.msg, "attachments"):
            return

        attachments = self.msg.attachments

        found_quoted_message = False
        for attachment in attachments:
            if "reply_id" in attachment and attachment['type'] == "reply":
                found_quoted_message = True
                break

        if not found_quoted_message:
            return

        reply_id = attachment['reply_id']
        group_id = self.msg.group_id

        msg = get_groupme_messages.get_exact_group_message(group_id, reply_id)
        self.referenced_message = RawMessage(msg['response']['message'])
        self.group_id = group_id

    def get_message_before_referenced_message(self):
        message_before = get_groupme_messages.get_list_of_messages_before(self.group_id, self.msg.message_id)
        return RawMessage(message_before['response']['message'])

    def _respond(self):
        pass
