
emojis = {
    "dino": [1, 62]
}

def return_emoticons(text, start):
    first = text.find(":", start + 1)
    if first > 0:
        second = text.find(":", first + 1)
        if second > 0:
            return [text[first+1:second]], return_emoticons(text, second)
    return None

def parse_message(text):
    values = {
          'bot_id' : 'f906f09e88ff3764c3c8b8c043',
    }
    emoticons = return_emoticons(text, 0)
    if emoticons is not None:
        emoticons = filter(None, emoticons)
        if len(emoticons) > 0:
            char_map = []
            for emoticon in emoticons:
                if emoticon[0] in emojis:
                    char_map.append(emojis[emoticon[0]])
                    text = text.replace(":" + emoticon[0] + ":","\ufffd",1)
            values["attachments"] = {
                'type' : 'emoji',
                'charmap' : char_map,
                'placeholder' : '\ufffd'
            }

    values["text"] = text
    return values