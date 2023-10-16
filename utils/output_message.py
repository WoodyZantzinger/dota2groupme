from enum import Enum, IntEnum


class Services(IntEnum):
    TEXT=0
    PHOTO_LOCAL=1
    PHOTO_URL=2
    VIDEO_LOCAL=3



class OutputMessage:
    def __init__(self, obj, obj_type=None, reply_to=None, spoiler=False):
        self.obj = obj
        self.obj_type = obj_type
        self.reply_to = reply_to
        self.spoiler = spoiler

    def execute(self, sender):
        func_lookup = {
            Services.TEXT: sender.send_text,
            Services.PHOTO_LOCAL: sender.send_photo_local,
            Services.PHOTO_URL: sender.send_photo_url,
            Services.VIDEO_LOCAL: sender.send_video_local
        }

        func = func_lookup[self.obj_type]
        if not sender.debug:
            func(self)
        else:
            print(self)
