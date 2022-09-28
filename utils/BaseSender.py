from utils.BaseMessage import BaseMessage

class BaseSender:

    def __init__(self, source_msg: BaseMessage, bot=None, debug=True):
        self.source_msg = source_msg
        self.debug = debug
        self.bot = bot
        pass

    def send_text(self, obj):
        raise NotImplemented("send_text not implemented for BaseSender object")

    def send_photo_local(self, obj):
        raise NotImplemented("send_photo_local not implemented for BaseSender object")

    def send_photo_url(self, obj):
        raise NotImplemented("send_photo_url not implemented for BaseSender object")

    def send_video_local(self, obj):
        raise NotImplemented("send_video_local not implemented for BaseSender object")



