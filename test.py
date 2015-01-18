#testhandler
from responses import *


def route_message(msg, sender):
    for cls in AbstractResponse.AbstractResponse.__subclasses__():
        print(cls)
        print(cls.is_relevant_msg(msg, sender))
        print(cls(msg, sender))

route_message("#last", "sty")