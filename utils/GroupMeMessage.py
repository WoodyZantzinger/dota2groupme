import json

emoji_data_file = "utils/groupme_emojis.json"

emojis_temp = None

GroupToBot = {}
GroupToBot["0"] = "f906f09e88ff3764c3c8b8c043" #Default

GroupToBot["13203822"] = "f906f09e88ff3764c3c8b8c043" #Main Group
GroupToBot["19216747"] = "200ba085c2b7a953cb74f849ad" #DnD Group
GroupToBot["23635322"] = "b9b8594507d45452e13dcb4012" #Cville Group
GroupToBot["13203822"] = "f906f09e88ff3764c3c8b8c043" #Dick.com group

# read the file to memory
with open(emoji_data_file) as f:
    emojis_temp = json.load(f)

# parse the strings to integers
for emoji in emojis_temp:
    emoji[0] = int(emoji[0])
    emoji[1] = int(emoji[1])

# reformat the dict to be what is expected by later code
# name : [idx0, idx1]

emojis = {}
for emoji in emojis_temp:
    emojis[emoji[2][1:-1]] = [emoji[0], emoji[1]]


def return_emoticons(text):
    return_val = []
    for emoji in emojis:
        first = text.find(emoji, 0)
        if first > -1:
            return_val.append(emoji)

    return return_val


def parse_message(text, groupID):
    values = {
          'bot_id': GroupToBot[groupID],
    }
    emoticons = return_emoticons(text)
    if len(emoticons) > 0:
        char_map = []
        for emoticon in emoticons:
            if emoticon in emojis:
                char_map.append(emojis[emoticon])
                text = text.replace(":" + emoticon + ":",u'\ufffd',1)
        values["attachments"] = [{
            'type': 'emoji',
            'charmap': char_map,
            'placeholder': u'\ufffd'
                                 }]

    values["text"] = text
    return values
