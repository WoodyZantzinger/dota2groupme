
emojis = {
    "dino": [1, 62]
}

def return_emoticons(text):
    return_val = []
    for emoji in emojis:
        first = text.find(emoji, 0)
        if first > -1:
            return_val.append(emoji)

    return return_val

def parse_message(text):
    values = {
          'bot_id' : 'f906f09e88ff3764c3c8b8c043',
    }
    emoticons = return_emoticons(text)
    if len(emoticons) > 0:
        char_map = []
        for emoticon in emoticons:
            if emoticon in emojis:
                char_map.append(emojis[emoticon])
                text = text.replace(":" + emoticon + ":",u'\ufffd',1)
        values["attachments"] = [{
            'type' : 'emoji',
            'charmap' : char_map,
            'placeholder' : u'\ufffd'
                                 }]

    values["text"] = text
    return values