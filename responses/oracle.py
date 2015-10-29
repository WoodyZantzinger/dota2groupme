from CooldownResponse import *
from utils.emulate.emulate import *

class oracle(ResponseCooldown):

    RESPONSE_KEY = "#oracle"

    COOLDOWN = 10 * 60

    def __init__(self, msg):
        super(oracle, self).__init__(msg, self.__module__, oracle.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            message = self.msg.text.partition("#oracle")[2]
            return generate_response(message, 0)
        else:
            print("not responding to #oracle because sender {} is on cooldown".format(self.msg.name))
