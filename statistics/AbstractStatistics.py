

class AbstractStatistics(object):

    ENABLED = True

    def __init__(self, messages, mod=None):
        super(AbstractStatistics, self).__init__()
        self.messages = messages

    def respond(self):
        return None

