# -*- coding: utf-8 -*

from .CooldownResponse import *
import openai


class ResponseChat(ResponseCooldown):

    message = "#gpt"

    RESPONSE_KEY = "#gpt"

    COOLDOWN = 1 * 60 * 60 * 3 / 2

    def __init__(self, msg):
        super(ResponseChat, self).__init__(msg, self, ResponseChat.COOLDOWN)

    def _respond(self):

        openai.api_key = DataAccess.get_secrets()['OPENAI_KEY']
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant who provides short, concise answers short enough to fit in a text message"},
                {"role": "user", "content": self.msg.text.partition(' ')[2]}
            ]
        )

        return response['choices'][0]['message']['content']
