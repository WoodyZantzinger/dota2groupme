
from .AbstractStatistics import *
import pprint

class StatisticMostHeartsGiven(AbstractStatistics):

    ENABLED = True

    def __init__(self, messages, mod=None):
        super(StatisticMostHeartsGiven, self).__init__(messages)
        self.messages = messages

    def respond(self):
        names_seen = dict()
        for msg in self.messages:
            for id in msg.favorited_by:
                if id not in names_seen:
                    names_seen[id] = [None, 0]
                name = names_seen[id][0]
                num = names_seen[id][1] + 1
                names_seen[id] = [name, num]
            if msg.user_id not in names_seen:
                names_seen[msg.user_id] = [msg.name, 0]
            num = names_seen[msg.user_id][1]
            names_seen[msg.user_id] = [msg.name, num]

        messages_list = []
        for k in names_seen:
            messages_list.append(names_seen[k])

        messages_list = sorted(messages_list, key=lambda msg:msg[1])
        hearts_number = messages_list[-1][1]
        heartiest = filter(lambda x:x[1]==hearts_number, messages_list)
        heartiest = [pair[0] for pair in heartiest]
        users_str = ','.join(map(str, heartiest))
        MSG_FORMAT = "Heartiest user(s) with {n} hearts: {users}"
        return MSG_FORMAT.format(n=hearts_number, users=users_str)


