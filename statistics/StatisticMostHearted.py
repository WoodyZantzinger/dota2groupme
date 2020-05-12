
from .AbstractStatistics import *

class StatisticMostHearted(AbstractStatistics):

    ENABLED = True

    def __init__(self, messages, mod=None):
        super(StatisticMostHearted, self).__init__(messages)
        self.messages = messages

    def respond(self):
        most_hearts = -1
        for msg in self.messages:
            hearts = msg.favorited_by
            if len(hearts) > most_hearts:
                most_hearts = len(hearts)
        msgs_with_hearts = filter(lambda msg:len(msg.favorited_by)==most_hearts, self.messages)

        ONE_MESSAGE_FMT = \
"""Most popular message, from {user}, with {nhearts} hearts:
\t{msg}"""
        MULTI_MESSAGE_FMT = \
"""Most popular messages, with {nhearts} hearts:
{msg}"""
        MULTI_INDIV_FMT = "\t{user}: {msg}\n"
        OUTMSG = None

        if len(msgs_with_hearts):
            if len(msgs_with_hearts) == 1:
                msg = msgs_with_hearts[0]
                user = msg.name
                text = msg.text
                OUTMSG = ONE_MESSAGE_FMT.format(user=user, nhearts=most_hearts, msg=text)
            else:
                bodymsg = ""
                if len(msgs_with_hearts) > 3:
                    bodymsg = "Too many!"
                else:
                    for msg in msgs_with_hearts:
                        user = msg.name
                        text = msg.text
                        bodymsg = bodymsg + MULTI_INDIV_FMT.format(user=user, msg=text)
                OUTMSG = MULTI_MESSAGE_FMT.format(nhearts=most_hearts, msg=bodymsg)
        return OUTMSG

