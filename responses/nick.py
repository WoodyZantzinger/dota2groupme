from .CooldownResponse import *


class ResponseNick(ResponseCooldown):

    RESPONSE_KEY = "#nick"

    COOLDOWN = 30 * 60

    def __init__(self, msg):
        super(ResponseNick, self).__init__(msg, self, ResponseNick.COOLDOWN)

    def _respond(self):
        # check if user is admin
        return
        text = self.msg.text
        parts = text.partition(ResponseNick.RESPONSE_KEY)
        new_nick = parts[1]
        self.msg.update_nick(new_nick)

        # if user is not admin, make user admin
        # if #nick in message, partition and act on it
        pass

    @classmethod
    def is_relevant_msg(cls, msg):
        return True
