from .CooldownResponse import *
from utils.emulate.emulate import *


class Oracle(ResponseCooldown):

    RESPONSE_KEY = "#oracle"

    COOLDOWN = 30 * 60

    def __init__(self, msg):
        super(Oracle, self).__init__(msg, self, Oracle.COOLDOWN)

    def _respond(self):
        if self.is_sender_off_cooldown():
            message = self.msg.text.partition("#oracle")[2]
            out = generate_response(message, 0)
            self.note_response(out)
            return out
        else:
            print("not responding to #oracle because sender {} is on cooldown".format(self.msg.name))
