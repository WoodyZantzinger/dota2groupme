from .CooldownResponse import *
from utils.emulate.emulate import *


class Oracle_Debug(ResponseCooldown):

    RESPONSE_KEY = "#debugoracle"

    COOLDOWN = 30 * 60

    def __init__(self, msg):
        super(Oracle_Debug, self).__init__(msg, self, Oracle_Debug.COOLDOWN)

    def _respond(self):
        message = self.msg.text.partition("#debugoracle")[2]
        out = generate_response(message, 1)
        return out

