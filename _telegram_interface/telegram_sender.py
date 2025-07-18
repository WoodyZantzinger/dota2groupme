import asyncio
import sys

from telegram import Bot

sys.path.append("..")
from utils.BaseSender import BaseSender


class TelegramSender(BaseSender):
    def __init__(self, source_msg, bot=None, debug=True):
        super().__init__(source_msg, bot, debug)

    def send_text(self, obj):
        asyncio.new_event_loop().run_until_complete(
            self.bot.send_message(chat_id=self.source_msg.group_id, text=obj.obj, reply_to_message_id=obj.reply_to)
        )

    def send_photo_local(self, obj):
        asyncio.new_event_loop().run_until_complete(
            self.bot.sendDocument(chat_id=self.source_msg.group_id, document=open(obj.obj, 'rb'), reply_to_message_id=obj.reply_to)
        )
    def send_photo_url(self, obj):
        asyncio.new_event_loop().run_until_complete(
            self.bot.send_animation(chat_id=self.source_msg.group_id, animation=obj.obj, reply_to_message_id=obj.reply_to, has_spoiler=obj.spoiler)
        )
    def send_video_local(self, obj):
        raise NotImplemented("send_video_local not implemented for BaseSender object")
