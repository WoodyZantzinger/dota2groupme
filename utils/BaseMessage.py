from enum import Enum


class Services(Enum):
    GROUPME = "GROUPME"
    TELEGRAM = "TELEGRAM"


class BaseMessage():
    def __init__(self):
        pass