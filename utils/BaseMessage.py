from enum import Enum

from utils import get_groupme_messages
from utils.rawmessage import RawMessage
from utils.GroupMeMessage import HostImage


class Services(Enum):
    GROUPME = ""
    TELEGRAM = "TELEGRAM"


def make_message(raw_msg: RawMessage):
    if raw_msg.from_servce == Services.GROUPME.value:
        return GroupMeMessage(raw_msg)
    elif raw_msg.from_servce == Services.TELEGRAM.value:
        raise NotImplemented
    else:
        raise NotImplemented("Couldn't parse message's service value: " + raw_msg.from_service)


class BaseMessage:
    def __init__(self, raw_msg: RawMessage):
        self.raw_msg = raw_msg
        self.response = None

    def is_quoted_message(self):
        raise NotImplemented

    def get_quoted_message(self):
        raise NotImplemented

    def attach_image(self, image_uri):
        raise NotImplemented

    def get_sender_uid(self):
        raise NotImplemented


class GroupMeMessage(BaseMessage):
    def __init__(self, raw_msg: RawMessage):
        super().__init__(raw_msg)

    def is_quoted_message(self):
        if not hasattr(self, "attachments"):
            return False

        for attachment in self.attachments:
            if "reply_id" in attachment and attachment['type'] == "reply":
                return True

        return False

    def get_quoted_message(self):
        for attachment in self.attachments:
            if "reply_id" in attachment and attachment['type'] == "reply":
                reply_id = attachment['reply_id']
                group_id = self.msg.group_id
                msg = get_groupme_messages.get_exact_group_message(group_id, reply_id)
                return make_message(RawMessage(msg['response']['message']))

    def attach_image(self, image_uri):
        self.response = HostImage(image_uri)


class TelegramMessage(BaseMessage):
    def __init__(self, raw_msg: RawMessage):
        super().__init__(raw_msg)

    def is_quoted_message(self):
        return not self.raw_msg.reply_to_message