import urllib.parse

from data import DataAccess
from .AbstractResponse import *
import requests
import os
import pickle
import asyncio

import callofduty
from callofduty import Mode, Platform, Title
import html

platform_map = {
    "battle": Platform.BattleNet,
    "uno": Platform.Activision,
}


def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


async def get_last_results(client_login, client_pass, platform, username):
    parts = username.split("#")
    username_simple = parts[0].lower()
    client = await callofduty.Login(client_login, client_pass)
    match_last = (await client.GetPlayerMatches(platform, username, Title.ModernWarfare, Mode.Warzone, limit=1))[0]
    match_result = await client.GetFullMatch(platform, Title.ModernWarfare, Mode.Warzone, match_last.id)
    players = match_result['allPlayers']
    for player in players:
        this_player_username = player['player']['username'].lower()
        if this_player_username == username_simple:
            break
        else:
            player = None

    if not player:
        return None

    match_performance_template = "{name} of clan {clan} finished {place}th with {kills} kills and {damage} damage. He "

    gulag = "didn't go to the gulag"
    place = "?"
    if "gulagKills" in player["playerStats"]:
        if player["playerStats"]["gulagKills"] > 0: gulag = "won his gulag (ez)"
        if player["playerStats"]["gulagDeaths"] > 0: gulag = "lost his gulag (bitch)"
        place = int(player["playerStats"]["teamPlacement"])
    else:
        gulag = "played some wierd mode"

    if "clantag" not in player["player"]: player["player"]["clantag"] = "looking for love"

    out = match_performance_template.format(
        name=player["player"]["username"],
        clan=player["player"]["clantag"],
        place=place,
        damage=player["playerStats"]["damageDone"],
        kills=int(player["playerStats"]["kills"])
    ) + gulag

    pass
    return out


class WarzoneLast(AbstractResponse):
    RESPONSE_KEY = "#zonelast"

    HELP_RESPONSE = "Shows your personal stats from the last game, add a user argument to find someone elses stats"

    def __init__(self, msg):
        super(WarzoneLast, self).__init__(msg, self)

    def _respond(self):
        print(f"msg.senderID = {self.msg.sender_id}")
        user = DataAccess.DataAccess().get_user("GROUPME_ID", self.msg.sender_id)
        COD_client_login = DataAccess.get_secrets()["COD_USER"]
        COD_client_pass = DataAccess.get_secrets()["COD_PASS"]
        canonical_name = user['Name']
        COD_name = user['COD_ID']

        if COD_name is None:
            return "I don't know your Call of Duty ID. Please get Mike or Woody to add it to the database. Look it up here and send your profile page:\nhttps://cod.tracker.gg/warzone"
        platform, username = COD_name.split(":")
        platform = platform_map[platform]
        username = urllib.parse.unquote(username)

        loop = get_or_create_eventloop()
        result = None
        try:
            result = loop.run_until_complete(
                get_last_results(COD_client_login, COD_client_pass, platform, username)
            )
        except:
            pass

        if not result:
            return f"Ensure the following are d1one:\n1: Your COD ID is set correctly (I think it is {COD_name}).\n2. Your profile settings are set to Friends/All/All under Battle.net account on this page: https://profile.callofduty.com/cod/profile. 3. You are friends with Mike (Riffin) on COD."
        return result
