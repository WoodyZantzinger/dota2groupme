
from .AbstractStatistics import *

class StatisticMostMessagesSent(AbstractStatistics):

    ENABLED = True

    def __init__(self, messages, mod=None):
        super(StatisticMostMessagesSent, self).__init__(messages)
        self.messages = messages

    def respond(self):
        names_to_n_messages = dict()
        for msg in self.messages:
            if not msg.user_id in names_to_n_messages:
                names_to_n_messages[msg.user_id] = [msg.name, 0]
            new_num = names_to_n_messages[msg.user_id][1] + 1
            names_to_n_messages[msg.user_id] = [msg.name, new_num]

        messages_list = []
        for k in names_to_n_messages:
            messages_list.append(names_to_n_messages[k])

        messages_list = sorted(messages_list, key=lambda msg:msg[1])
        chattiest_number = messages_list[-1][1]
        chattiest = filter(lambda x:x[1]==chattiest_number, messages_list)
        chattiest = [pair[0] for pair in chattiest]
        users_str = ','.join(map(str, chattiest))
        MSG_FORMAT = "Chattiest user(s) with {n} messages: {users}"
        return MSG_FORMAT.format(n=chattiest_number, users=users_str)


