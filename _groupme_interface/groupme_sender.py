import json
import sys
import time
import urllib

import requests

from data import DataAccess
from utils.BaseMessage import BaseMessage

sys.path.append("..")
from utils.BaseSender import BaseSender
from utils import GroupMeMessage


def HostImage(url, local=False):
    GM_key = DataAccess.get_secrets()['GROUPME_AUTH']

    if not local:
        r = requests.get(url)
        content = r.content
    else:
        with open(url, 'rb') as f:
            content = f.read()
    url = 'https://image.groupme.com/pictures'

    header = {'X-Access-Token': GM_key, 'Content-Type': 'image/gif'}
    try:
        req = urllib.request.Request(url, content, header)
        response = urllib.request.urlopen(req)
        JSON_response = json.load(response)
        return JSON_response["payload"]["picture_url"]
    except urllib.error.HTTPError:
        print("There was some sort of error uploading the photo")
        # print(r.content) lmao xd
        return ""


class GroupMeSender(BaseSender):

    def __init__(self, source_msg: BaseMessage, bot=None, debug=True):
        super().__init__(source_msg, bot, debug)

    def send_text(self, obj):
        time.sleep(1)
        try:
            print(u"Sending: '{}".format(obj))
        except Exception as e:
            line_fail = sys.exc_info()[2].tb_lineno
            print("\tError: {} on line {}".format(repr(e), line_fail))

        groupID = self.source_msg.group_id
        key = DataAccess.get_secrets()["GROUPME_AUTH"]
        url = 'https://api.groupme.com/v3/groups/{id}/messages?token={token}'.format(id=groupID, token=key)

        values = GroupMeMessage.parse_message(obj, groupID)

        final_values = {"message": values}

        if not self.debug:
            r = requests.post(url, json=final_values)
            print(r.status_code, r.reason)
            return r.status_code
        else:
            return 'Win'

    def send_photo_url(self, obj):
        time.sleep(1)
        self.send_text(obj)

    def send_photo_local(self, obj):
        time.sleep(1)
        hosted_str = HostImage(obj)
        self.send_text(hosted_str)
