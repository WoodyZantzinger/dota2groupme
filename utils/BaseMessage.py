import urllib
import uuid
from enum import Enum

from telegram import PhotoSize, Document

from utils import get_groupme_messages
from utils.rawmessage import RawMessage
from _telegram_interface.telegram_listener import reformat_telegram_message
from data import DataAccess

class Services(Enum):
    GROUPME = ""
    TELEGRAM = "TELEGRAM"


def make_message(raw_msg: RawMessage):
    from_service = raw_msg.from_service
    if from_service == Services.GROUPME.value:
        return GroupMeMessage(raw_msg)
    elif from_service == Services.TELEGRAM.value:
        tgm = TelegramMessage(raw_msg)
        return tgm
    else:
        raise NotImplemented("Couldn't parse message's service value: " + raw_msg.from_service)


class BaseMessage:
    def __init__(self, raw_msg: RawMessage):
        self.response = None
        for k in raw_msg.__dict__:
            setattr(self, k, getattr(raw_msg, k))

    def is_quoted_message(self):
        raise NotImplemented("Message class doesn't have implementation for is_quoted_message")

    def get_quoted_message(self):
        raise NotImplemented("Message class doesn't have implementation for get_quoted_message")

    def save_attachments_to_local(self):
        raise NotImplemented("Message class doesn't have implementation for get_attached_image_urls")

    def get_sender_uid(self):
        raise NotImplemented("Message class doesn't have implementation for get_sender_uid")


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


    def save_attachments_to_local(self):
        if not hasattr(self, "attachments"):
            return

        attachments = self.attachments

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
        msg = msg['response']['message']
        image_attachments = []
        if "attachments" in msg:
            for attachment in msg['attachments']:
                if attachment['type'] == "image":
                    image_attachments.append(attachment)
        image_attachments

        local_fnames = []
        for attachment in image_attachments:
            uuid = attachment['url'].split('.')[-1]
            fname = attachment['url'][:(-1 * (len(uuid) + 1))]
            ftype = fname.split('.')[-1]
            save_fname = "".join([uuid, '.', ftype])
            urllib.request.urlretrieve(attachment['url'],
                                       save_fname)
            local_fnames.append(save_fname)
        return local_fnames

    def get_sender_uid(self):
        return self.sender_id


class TelegramMessage(BaseMessage):
    def __init__(self, raw_msg: RawMessage):
        super().__init__(raw_msg)

    def is_quoted_message(self):
        return not self.raw_msg.reply_to_message

    def get_quoted_message(self):
        reply_json = self.raw_msg['message']['reply_to_message']
        formatted_json = reformat_telegram_message(reply_json)
        return TelegramMessage(formatted_json)

    async def save_attachments_to_local(self, bot=None):
        print("oh, hello there.")
        attachments = self.raw_msg['message']['effective_attachment']
        attached_items = []
        if type(attachments) == list:
            file_ids = set([item['file_id'][0:15] for item in attachments])
            for fid in file_ids:
                photo_set = [item for item in attachments if item['file_id'][0:15] == fid]
                image_sizes = [item['file_size'] for item in photo_set]
                largest_item = [item for item in photo_set if item['file_size'] == max(image_sizes)][0]
                ps = PhotoSize(
                    largest_item['file_id'],
                    largest_item['file_unique_id'],
                    largest_item['width'],
                    largest_item['height'],
                    largest_item['file_size'],
                )
                attached_items.append(ps)
        else:
            doc = Document(
                file_id=attachments['file_id'],
                file_unique_id=attachments["file_unique_id"],
                thumb=None,
                file_name=attachments["file_name"],
                mime_type=attachments["mime_type"],
                file_size=attachments["file_size"],
                bot=bot
            )
            attached_items.append(doc)

        out_fnames = []
        print(attached_items)
        for item in attached_items:
            save_name = ""
            try:
                save_name = item.file_name
            except:
                save_name = str(uuid.uuid4()) + ".png"
            # @TODO add a bot object to the photothing initialization so it can save?
            print(save_name)
            obj = await bot.get_file(file_id=item.file_id)
            fname = await obj.download()
            print(fname)
            out_fnames.append(fname.name)
        return out_fnames

    def get_sender_uid(self):
        # def telegram id
        tid = self.raw_msg['sender_id']
        # get user from database given tid
        da = DataAccess.DataAccess()
        user = da.get_user("TELEGRAM_ID", tid)
        # get groupme id from user object?
        return user["GROUPME_ID"]