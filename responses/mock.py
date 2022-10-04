import random
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import os
import urllib
from data import DataAccess
import json
from responses.CooldownResponse import ResponseCooldown
from responses.QuoteResponse import ResponseQuote
from utils import get_groupme_messages, output_message
import tempfile

font_path = os.path.join('meme_resources', 'Fonts', 'Impact', 'impact.ttf')

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
    img = Image.open(filename)
    image_size = img.size

    IDEAL_LINE_CHARACTERS = 40
    X_BUFFER_RANGE = 10

    # break mocked text into new lines and mess up the cases
    bottom_string = mockify_text(bottom_string)
    bottom_strings = split_string(bottom_string, IDEAL_LINE_CHARACTERS)
    bottom_strings = [s for s in bottom_strings if len(s.strip())]

    # find biggest font size that works
    # guess at a starting point
    font_size = int(image_size[1] / 5)
    font = ImageFont.truetype(font_path, font_size)
    MAX_X_SIZE = image_size[0] - X_BUFFER_RANGE
    while not all([font.getsize(s)[0] < MAX_X_SIZE for s in bottom_strings]):
        font_size = font_size - 1
        font = ImageFont.truetype(font_path, font_size)

    # create the final image
    # draw the template image
    draw = ImageDraw.Draw(img)

    outline_range = int(font_size / 15)
    min_y_position = image_size[1] - outline_range

    # for each line of text, starting at the bottom
    for line in reversed(bottom_strings):
        # figure out where to position text
        text_size = font.getsize(line)
        position_x = (image_size[0] / 2) - (text_size[0] / 2)
        position_y = min_y_position - text_size[1]
        text_position = (position_x, position_y)
        min_y_position = position_y - outline_range

        # draw black background (I think this is very slow?)
        for x in range(-outline_range, outline_range + 1):
            for y in range(-outline_range, outline_range + 1):
                draw.text((text_position[0] + x, text_position[1] + y), line, (0, 0, 0), font=font)

        # draw white text over black background
        draw.text(text_position, line, (255, 255, 255), font=font)

    # write temp file to disk and return filename
    temp_name = next(tempfile._get_candidate_names()) + ".png"
    img.save(temp_name)
    return temp_name


def make_spongebob_image(message_to_mock):
    spongebob_path = os.path.join('meme_resources', 'ImageLibrary', 'mocking_spongebob.png')
    path = make_meme("", message_to_mock, spongebob_path)
    return path


class ResponseMock(ResponseQuote):
    COOLDOWN = 2 * 60 * 60
    RESPONSE_KEY = "#mock"
    SUN_UPLOADS_FOLDER_ID = ''

    def __init__(self, msg):
        super(ResponseMock, self).__init__(msg, ResponseMock.COOLDOWN)
        self.quoting_own_message = False


    def _respond(self):
        referenced_text = self.get_referenced_message_text()
        if referenced_text and not self.quoting_own_message:
            filename = make_spongebob_image(referenced_text)
            return output_message.OutputMessage(filename, output_message.Services.PHOTO_LOCAL)
            # hosted_image_path = HostImage(filename, local=True)
            # os.remove(filename)
            # return hosted_image_path
        if self.quoting_own_message:
            print("Not responding because user is quoting their own message")

