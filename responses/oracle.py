from .CooldownResponse import *
from utils.emulate.emulate import *


class Oracle(ResponseCooldown):

    RESPONSE_KEY = "#oracle"

    COOLDOWN = 30 * 60

    def __init__(self, msg):
        super(Oracle, self).__init__(msg, self, Oracle.COOLDOWN)

    def _respond(self):
        message = self.msg.text.partition("#oracle")[2]
        out = generate_response(message, 0)
        return out
