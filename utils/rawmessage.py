# -*- coding: utf-8 -*-
import jsonpickle

from utils import GroupMeMessage


class RawMessage(object):

    def __init__(self, rawjson):
        super(RawMessage, self).__init__()

        self.rawjson = rawjson


        self.attachments = None
        self.avatar_url = None
        self.created_at = None
        self.group_id = None
        self.id = None
        self.name = None
        self.sender_id = None
        self.sender_type = None
        self.source_guid = None
        self.system = None
        self.text = None
        self.user_id = None
        self.from_service = ""  # @TODO CHANGE THIS TO NONE ALSO

        for item in self.rawjson.keys():
            if (item == "TELEGRAM_SERIALIZED_MESSAGE"):
                value = jsonpickle.decode(self.rawjson[item])
                setattr(self, item, value)
            else:
                setattr(self, item, self.rawjson[item])
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



