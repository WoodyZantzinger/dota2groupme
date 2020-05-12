
from .AbstractStatistics import *

class StatisticMessagesSent(AbstractStatistics):

    ENABLED = True

    def __init__(self, messages, mod=None):
        super(StatisticMessagesSent, self).__init__(messages)
        self.messages = messages

    def respond(self):
        n = len(self.messages)
        MSG_FORMAT = "Total number of messages sent: {n}"
        return MSG_FORMAT.format(n=n)


