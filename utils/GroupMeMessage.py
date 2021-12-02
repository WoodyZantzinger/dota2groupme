import json
import urllib

import requests

from data import DataAccess

emoji_data_file = "utils/groupme_emojis.json"

emojis_temp = None

GroupToBot = {}
GroupToBot["0"] = "f906f09e88ff3764c3c8b8c043"  # Default

GroupToBot["13203822"] = "f906f09e88ff3764c3c8b8c043"  # Main Group
GroupToBot["19216747"] = "200ba085c2b7a953cb74f849ad"  # DnD Group
GroupToBot["23635322"] = "b9b8594507d45452e13dcb4012"  # Cville Group
GroupToBot["16905359"] = "2cfa6c35347bffeb718a9061d2"  # Dick.com group
GroupToBot["11861464"] = "3498b59720bc9473c86f631600"  # Test group
GroupToBot["32229954"] = "bd982e70861fa051c78e389565"  # PUBG

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

def HostImage(url):
    GM_key = DataAccess.get_secrets()['GROUPME_AUTH']

    r = requests.get(url)
    url = 'https://image.groupme.com/pictures'

    header = {'X-Access-Token': GM_key, 'Content-Type': 'image/gif'}
    try:
        req = urllib.request.Request(url, r.content, header)
        response = urllib.request.urlopen(req)
        JSON_response = json.load(response)
        return (JSON_response["payload"]["picture_url"])
    except urllib.error.HTTPError:
        print("There was some sort of error uploading the photo")
        print(r.content)
        return ""

def return_emoticons(text):
    return_val = []
    for emoji in emojis:
        first = text.find(emoji, 0)
        if first > -1:
            return_val.append(emoji)

    return return_val


def parse_message(text, groupID):
    values = {}
    emoticons = return_emoticons(text)
    if len(emoticons) > 0:
        char_map = []
        for emoticon in emoticons:
            if emoticon in emojis:
                char_map.append(emojis[emoticon])
                text = text.replace(":" + emoticon + ":", u'\ufffd', 1)
        values["attachments"] = [{
            'type': 'emoji',
            'charmap': char_map,
            'placeholder': u'\ufffd'
        }]

    values["text"] = text
    # split TEXT at spaces
    # see if any of the splits contain i.groupme.com
    # IF SO, blank out ONLY THAT space
    # add url to attachment
    # re-join rest of message

    message_parts = text.split()
    hosted_images_idxs = []
    for i, part in enumerate(message_parts):
        if "https://i.groupme.com/" in part:
            hosted_images_idxs.append(i)
    if len(hosted_images_idxs) != 0:
        attachments = []
        for idx in hosted_images_idxs:
            attach =    {
                        'type': 'image',
                        'url': message_parts[i]
                        }
            attachments.append(attach)
            text = text.replace(message_parts[i], "")
        values["text"] = text.strip()
        values["attachments"] = attachments

    #if ("https://i.groupme.com/" in text and " " not in text):
    #    values["attachments"] = [{
    #        'type': 'image',
    #        'url': text
    #    }]
    #    values["text"] = ""

    return values
