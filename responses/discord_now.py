# -*- coding: utf-8 -*
from .AbstractResponse import AbstractResponse
import requests
import steamapi
import os
import asyncio
import discord


class DiscordNow(AbstractResponse):

    RESPONSE_KEY = "#dnow"

    def __init__(self, msg):
        super(DiscordNow, self).__init__(msg)

    def respond(self):
        global out
        out = ""
        asyncio.set_event_loop(asyncio.new_event_loop())
        client = discord.Client()

        @client.event
        async def on_ready():
            global out
            print('We have logged in as {0.user}'.format(client))

            # who is in channels right now?
            for id, channel in client.guilds[0]._channels.items():
                if isinstance(channel, discord.VoiceChannel) and len(channel.members) > 0:
                    out += (channel.name + ": ")
                    for member in channel.members:
                        out += ("\n    - " + member.name)
            await client.logout()

        key = AbstractResponse.local_var["DISCORD"]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(client.start(key))

        #asyncio.run(client.start(key))

        if not out:
            return "Nobody's online :("
        return out


