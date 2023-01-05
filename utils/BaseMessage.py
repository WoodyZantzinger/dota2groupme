import urllib
import uuid
from enum import Enum

from telegram import PhotoSize, Document, _bot

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

    def get_quoted_message_text(self):
        raise NotImplemented("Message class doesn't have implementation for get_quoted_message_text")

    def get_quoted_message_sender_uid(self):
        raise NotImplemented("Message class doesn't have implementation for get_quoted_message_sender_uid")

    def save_attachments_to_local(self):
        raise NotImplemented("Message class doesn't have implementation for get_attached_image_urls")

    def get_sender_uid(self):
        raise NotImplemented("Message class doesn't have implementation for get_sender_uid")

    def update_nick(self):
        raise NotImplemented("Message class doesn't have implementation for update_nick")


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

    def get_quoted_message_text(self):
        for attachment in self.attachments:
            if "reply_id" in attachment and attachment['type'] == "reply":
                reply_id = attachment['reply_id']
                group_id = self.msg.group_id
                msg = get_groupme_messages.get_exact_group_message(group_id, reply_id)
                return RawMessage(msg['response']['message']).text

    def get_quoted_message_sender_uid(self):
        for attachment in self.attachments:
            if "reply_id" in attachment and attachment['type'] == "reply":
                reply_id = attachment['reply_id']
                group_id = self.msg.group_id
                msg = get_groupme_messages.get_exact_group_message(group_id, reply_id)
                return RawMessage(msg['response']['message']).sender_id

    def get_quoted_message_id(self):
        for attachment in self.attachments:
            if "reply_id" in attachment and attachment['type'] == "reply":
                reply_id = attachment['reply_id']
                group_id = self.msg.group_id
                msg = get_groupme_messages.get_exact_group_message(group_id, reply_id)
                return RawMessage(msg['response']['message']).id

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
        self.tg_bot = _bot.Bot(DataAccess.get_secrets()["TELEGRAM_API_KEY"])

    def is_quoted_message(self):
        return "reply_to_message" in self.message

    def get_quoted_message(self):
        reply_json = self.message['reply_to_message']
        formatted_json = reformat_telegram_message(reply_json)
        return TelegramMessage(formatted_json)

    def get_quoted_message_text(self):
        return self.message['reply_to_message']['text']

    def get_quoted_message_sender_uid(self):
        tid = self.message['reply_to_message']['from_user']['id']
        da = DataAccess.DataAccess()
        user = da.get_user("TELEGRAM_ID", tid)
        # get groupme id from user object?
        if user and "GROUPME_ID" in user.values:
            return user['GROUPME_ID']
        else:
            return None

    def get_quoted_message_id(self):
        return self.message['reply_to_message']['id']

    @staticmethod
    async def save_photos(obj):
        attachments = obj.effective_message['reply_to_message']['effective_attachment']
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
            f_obj = await obj.tg_bot.get_file(file_id=item.file_id)
            fname = await f_obj.download()
            print(fname)
            out_fnames.append(fname.name)
        return out_fnames

    @staticmethod
    async def save_video(obj):
        pass

    @staticmethod
    async def save_audio(obj):
        pass

    async def save_attachments_to_local(self):
        print("oh, hello there.")
        attachments = self.effective_message['reply_to_message']['effective_attachment']
        attached_items = []
        # types = {
        #     'photo': TelegramMessage.save_photos,
        #     'video': TelegramMessage.save_video,
        #     'video_note': TelegramMessage.save_video,
        #     'voice': TelegramMessage.save_audio,
        #     'audio': TelegramMessage.save_audio,
        # }
        #
        # fnames = []
        # for key in types:
        #     if key in self.effective_message['reply_to_message']:
        #         fnames.append(types[key](self))


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
                # file_name=attachments["file_name"],
                # mime_type=attachments["mime_type"],
                file_size=attachments["file_size"],
                bot=self.tg_bot
            )
            attached_items.append(doc)

        out_fnames = []
        print(attached_items)
        for item in attached_items:
            # save_name = ""
            # try:
            #     save_name = item.file_name
            # except:
            #     save_name = str(uuid.uuid4()) + ".png"
            # # @TODO add a bot object to the photothing initialization so it can save?
            # print(save_name)
            obj = await self.tg_bot.get_file(file_id=item.file_id)
            fname = await obj.download()
            print(fname)
            out_fnames.append(fname.name)
        return out_fnames

    def get_sender_uid(self):
        # def telegram id
        tid = self.sender_id
        # get user from database given tid
        da = DataAccess.DataAccess()
        user = da.get_user("TELEGRAM_ID", tid)
        # get groupme id from user object?
        if user and "GROUPME_ID" in user.values:
            return user['GROUPME_ID']
        else:
            return None
