import datetime
import time

from responses.QuoteResponse import ResponseQuote


class ResponseSuperheart(ResponseQuote):

    RESPONSE_KEY = "#superheart"

    def __init__(self, msg):
        super(ResponseSuperheart, self).__init__(msg)

    def _respond(self):
        if not self.referenced_message:
            return

        msg_to_give_to = self.referenced_message
        if self.referenced_message.name == "sUN":
            msg_to_give_to = self.get_message_before_referenced_message()

        recipient_id = msg_to_give_to.sender_id
        recipient_name = msg_to_give_to.name

        sender_id = self.msg.sender_id
        sender_name = self.msg.name

        if (recipient_id == sender_id):
            return "Cannot superheart own message."

        coin_storage = self.get_response_storage("coins")
        if not coin_storage:
            coin_storage = dict()

        # check if giver can give:
            # first, are users in coin storage?
            # set up user if not already
        TOKEN_LOOKUP_KEY = "last_free_token_time"
        TOKEN_COUNT_KEY = "token_count"
        for id in [sender_id, recipient_id]:
            if id not in coin_storage:
                coin_storage[id] = {}
            if TOKEN_LOOKUP_KEY not in coin_storage[id]:
                coin_storage[id][TOKEN_LOOKUP_KEY] = None
            if TOKEN_COUNT_KEY not in coin_storage[id]:
                coin_storage[id][TOKEN_COUNT_KEY] = 0

            # sort out if can send, and cost if so
        can_send_token = False
        sending_cost = 1

        ymd_format = '%Y-%m-%d'
        now_time = int(time.time())
        now_time = datetime.datetime.utcfromtimestamp(now_time).strftime(ymd_format)
        now_time = datetime.datetime.strptime(now_time, ymd_format)
        now_time = int(time.mktime(now_time.timetuple()))

        if not coin_storage[sender_id][TOKEN_LOOKUP_KEY]:
            can_send_token = True
            sending_cost = 0
        else:
            last_send_date = coin_storage[sender_id][TOKEN_LOOKUP_KEY]
            if now_time != last_send_date:
                can_send_token = True
                sending_cost = 0
            elif coin_storage[sender_id][TOKEN_COUNT_KEY] > 0:
                can_send_token = True
                sending_cost = 1

        if sending_cost == 0:
            coin_storage[sender_id][TOKEN_LOOKUP_KEY] = now_time

        if not can_send_token:
            return f"{sender_name} cannot send tokens now."
            return

        # adjust senders counts
        sender_tokens = coin_storage[sender_id][TOKEN_COUNT_KEY] - sending_cost
        recipient_tokens = coin_storage[recipient_id][TOKEN_COUNT_KEY] + 1

        coin_storage[sender_id][TOKEN_COUNT_KEY] = sender_tokens
        coin_storage[recipient_id][TOKEN_COUNT_KEY] = recipient_tokens
        coin_storage[sender_id]['name'] = sender_name
        coin_storage[recipient_id]['name'] = recipient_name

        self.set_response_storage("coins", coin_storage)

        return f"Transferred from {sender_name}[{sender_tokens}] to {recipient_name}[{recipient_tokens}]"