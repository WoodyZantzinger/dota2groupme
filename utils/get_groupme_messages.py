from data import DataAccess
import requests
import json

EXACT_MESSAGE_ENDPOINT = "https://api.groupme.com/v3/groups/{group_id}/messages/{msg_id}"
LIST_OF_MESSAGES_ENDPOINT = "https://api.groupme.com/v3/groups/{group_id}/messages"


def get_exact_group_message(group_id, message_id):
    url = EXACT_MESSAGE_ENDPOINT.format(
        group_id=group_id,
        msg_id=message_id
    )
    key = DataAccess.get_secrets()["GROUPME_AUTH"]

    values = {
        "token": key,
        "limit": 1,
    }

    req = requests.get(url, params=values)
    response = json.loads(req.text)
    return response

def get_list_of_messages_before(group_id, message_id, limit=1):
    url = LIST_OF_MESSAGES_ENDPOINT.format(
        group_id=group_id,
    )
    key = DataAccess.get_secrets()["GROUPME_AUTH"]

    values = {
        "before_id": message_id,
        "token": key,
        "limit": limit,
    }

    req = requests.get(url, params=values)
    response = json.loads(req.text)
    return response