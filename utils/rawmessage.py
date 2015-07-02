# -*- coding: utf-8 -*-



class RawMessage(object):

    def __init__(self, rawjson):
        super(RawMessage, self).__init__()
        self.rawjson = rawjson
        self.attachments = self.rawjson['attachments']
        self.avatar_url = self.rawjson['avatar_url']
        self.created_at = self.rawjson['created_at']
        self.group_id = self.rawjson['group_id']
        self.id = self.rawjson['id']
        self.name = self.rawjson['name']
        self.sender_id = self.rawjson['sender_id']
        self.sender_type = self.rawjson['sender_type']
        self.source_guid = self.rawjson['source_guid']
        self.system = self.rawjson['system']
        self.text = self.rawjson['text']
        self.user_id = self.rawjson['user_id']



