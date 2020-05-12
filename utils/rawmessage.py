# -*- coding: utf-8 -*-
from utils import GroupMeMessage


class RawMessage(object):

    def __init__(self, rawjson):
        super(RawMessage, self).__init__()

        self.rawjson = rawjson

        for item in self.rawjson.keys():
            setattr(self, item, self.rawjson[item])
        """

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
        """
        self.replace_emojis()

    def replace_emojis(self):
        #note the escape character for groupme emojis
        esc = u'\ufffd'
        #split the message on the escape character -- each item needs an :emoji: put between them
        if not self.text:
            return
        splittext = self.text.split(esc)

        #allocate a variable for the replacement mappings
        replacemap = None

        for attachment in self.attachments:
            if attachment['type'] == u'emoji':
                replacemap = attachment['charmap']

        #if there isn't one, just bail - nothing to replace
        if not replacemap:
            return

        # if for some reason the number of attachments doesn't match the number of $esc's, bail
        if self.text.count(esc) != len(replacemap):
            print("escape characters does not matches replacemap length!")
            print("not modifying characters in message")
            return

        # reverse lookup the :emoji: texts from the [1, 61]-like attachment mappings
        replacementtext = []
        for replace in replacemap:
            for emoji in GroupMeMessage.emojis:
                if GroupMeMessage.emojis[emoji] == replace:
                    replacementtext.append(emoji)

        # if something failed to look up, just bail
        if len(replacementtext) != len(replacemap):
            return

        out = []
        for i, chunk in enumerate(splittext):
            out.append(chunk)
            if (i != (len(splittext) - 1)):
                out.append(":" + replacementtext[i] + ":")
        self.text = "".join(out)



