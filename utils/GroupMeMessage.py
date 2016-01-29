import json

emoji_data_file = "utils/groupme_emojis.json"

emojis_temp = None

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


def parse_message(text):
    values = {
          'bot_id': '86321846d479dac3c4fe36909b',
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
