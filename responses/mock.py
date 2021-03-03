import random
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import os
import urllib
from data import DataAccess
import json
from responses.CooldownResponse import ResponseCooldown
from utils import get_groupme_messages

font_path = os.path.join('meme_resources', 'Fonts', 'Impact', 'impact.ttf')
print(f"Impact font path location: {font_path}")


def HostImage(path):
    GM_key = DataAccess.get_secrets()['GROUPME_AUTH']

    image_content = None
    with open(path, 'rb') as f:
        image_content = f.read()

    url = 'https://image.groupme.com/pictures'

    header = {'X-Access-Token': GM_key, 'Content-Type': 'image/png'}
    try:
        req = urllib.request.Request(url, image_content, header)
        response = urllib.request.urlopen(req)
        JSON_response = json.load(response)
        return (JSON_response["payload"]["picture_url"])
    except urllib.error.HTTPError:
        print("There was some sort of error uploading the photo")
        print(image_content)
        return ""


def mockify_text(text):
    output = ""
    for char in text:
        if char.isalpha():
            if random.random() > 0.5:
                char = char.upper()
            else:
                char = char.lower()
        output += char
    return output


def split_string(string, line_size):
    parts = []
    while True:
        try:
            breakpt = string[line_size:].index(" ")
            parts.append(string[:(breakpt + line_size)])
            string = string[(breakpt + line_size):]
        except:
            parts.append(string)
            break
    return parts


def make_meme(top_string, bottom_string, filename):
    bottom_string = mockify_text(bottom_string)
    img = Image.open(filename)
    image_size = img.size

    IDEAL_LINE_CHARACTERS = 40
    X_BUFFER_RANGE = 10

    bottom_strings = split_string(bottom_string, IDEAL_LINE_CHARACTERS)

    bottom_strings = [s for s in bottom_strings if len(s.strip())]

    # find biggest font size that works
    font_size = int(image_size[1] / 5)
    font = ImageFont.truetype(font_path, font_size)
    MAX_X_SIZE = image_size[0] - X_BUFFER_RANGE
    while not all([font.getsize(s)[0] < MAX_X_SIZE for s in bottom_strings]):
        font_size = font_size - 1
        font = ImageFont.truetype(font_path, font_size)

    draw = ImageDraw.Draw(img)
    min_y_position = image_size[1]
    outline_range = int(font_size / 15)

    for line in reversed(bottom_strings):
        text_size = font.getsize(line)
        position_x = (image_size[0] / 2) - (text_size[0] / 2)
        position_y = min_y_position - text_size[1]
        text_position = (position_x, position_y)
        min_y_position = position_y - outline_range

        for x in range(-outline_range, outline_range + 1):
            for y in range(-outline_range, outline_range + 1):
                draw.text((text_position[0] + x, text_position[1] + y), line, (0, 0, 0), font=font)
        draw.text(text_position, line, (255, 255, 255), font=font)

    img.save("temp.png")
    return "temp.png"


def make_spongebob_image(message_to_mock):
    spongebob_path = os.path.join('meme_resources', 'ImageLibrary', 'mocking_spongebob.png')
    path = make_meme("", message_to_mock, spongebob_path)
    return path


class ResponseMock(ResponseCooldown):
    COOLDOWN = 10 * 60
    RESPONSE_KEY = "#mock"
    SUN_UPLOADS_FOLDER_ID = ''

    def __init__(self, msg):
        super(ResponseMock, self).__init__(msg, self, ResponseMock.COOLDOWN)

    def get_referenced_text(self):
        if not hasattr(self.msg, "attachments"):
            return

        attachments = self.msg.attachments

        found_quoted_message = False
        for attachment in attachments:
            if "reply_id" in attachment and attachment['type'] == "reply":
                found_quoted_message = True
                break

        if not found_quoted_message:
            return

        reply_id = attachment['reply_id']
        group_id = self.msg.group_id

        msg = get_groupme_messages.get_exact_group_message(group_id, reply_id)
        msg = msg['response']['message']
        return msg['text']

    def _respond(self):
        refereced_text = self.get_referenced_text()
        filename = make_spongebob_image(refereced_text)
        return HostImage(filename)
