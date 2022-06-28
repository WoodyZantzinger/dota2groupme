# -*- coding: utf-8 -*
import pprint

from .AbstractResponse import AbstractResponse
import requests
import steamapi
import os
import asyncio
import discord
from data import DataAccess
import traceback

class DiscordNow(AbstractResponse):

    RESPONSE_KEY = "#dnow"

    def __init__(self, msg):
        super(DiscordNow, self).__init__(msg)

    def _respond(self):
        global out
        global msg

        out = ""
        msg = ""
        asyncio.set_event_loop(asyncio.new_event_loop())
        intents = discord.Intents.all()
        intents.members = True
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            try:
                global out
                global msg
                # print('We have logged in as {0.user}'.format(client))

                DiscordIdToName = DataAccess.DataAccess().get_x_to_y_map('DISCORD_ID', 'Name')
                activity_groups = dict()
                for member in client.guilds[0].members:
                    # downselect activities by only getting `playing` type activities -- others exist
                    playing_activities = [act for act in member.activities if (act.type is discord.ActivityType.playing)]
                    # care if 1) we have activities, and 2) the user is someone in the mapping
                    if playing_activities and (str(member.id) in DiscordIdToName):
                        readable_name = DiscordIdToName[str(member.id)]
                        activity = playing_activities[0] # for some reason, CoD has two entries, so just take the 0th
                        if activity.name in activity_groups:
                            activity_groups[activity.name].append(readable_name)
                        else:
                            activity_groups[activity.name] = [readable_name]

                msg = ""
                for group in activity_groups:
                    msg += f"\nGame {group}:"
                    for name in activity_groups[group]:
                        msg += f"\n\t- {name}"
                msg = msg.strip()

                # who is in channels right now?
                for id, channel in client.guilds[0]._channels.items():
                    if isinstance(channel, discord.VoiceChannel) and len(channel.members) > 0:
                        out += ('\nChat ' + channel.name + ": ")
                        for member in channel.members:
                            out += ("\n    - " + member.name)
                out = out.strip()
                await client.logout()
            except Exception as e:
                print("error in #dnow:")
                traceback.print_exc()

        secrets = DataAccess.get_secrets()
        key = secrets["DISCORD"]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(client.start(key))

        #asyncio.run(client.start(key))

        out = out + '\n' + msg
        out = out.strip()
        if not out:
            return "Nobody's online :("
        return out


