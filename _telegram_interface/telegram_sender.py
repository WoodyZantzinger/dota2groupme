import asyncio
import sys

from telegram import Bot

sys.path.append("..")
from utils.BaseSender import BaseSender


class TelegramSender(BaseSender):
    def __init__(self, base_message, bot: Bot):
        super().__init__(base_message, bot)

    def send_text(self, obj):
        asyncio.run(self.bot.send_message(chat_id=self.base_message.group_id, text=obj))
        raise NotImplemented("send_text not implemented for BaseSender object")

    def send_photo_local(self, obj):
        raise NotImplemented("send_photo_local not implemented for BaseSender object")

    def send_photo_url(self, obj):
        raise NotImplemented("send_photo_url not implemented for BaseSender object")

    def send_video_local(self, obj):
        raise NotImplemented("send_video_local not implemented for BaseSender object")
