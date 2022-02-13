# -*- coding: utf-8 -*
from data import DataAccess
from .AbstractResponse import AbstractResponse
import os
import json
import requests
from pubg_python import PUBG, Shard

class ResponsePUBGLast(AbstractResponse):
    RESPONSE_KEY = "#pubglast"

    def __init__(self, msg):
        super(ResponsePUBGLast, self).__init__(msg)

    def _respond(self):
        out = ""

        template = "{name} did {damage} damage for {numKills} kills (placing {killRank} in kills) to finish {result} in a {gameType}. Squad:\n{squad}"

        user = DataAccess.DataAccess().get_user("GROUPME_ID", self.msg.sender_id)
        canonical_name = user['Name']
        PUBGname = user['PUBG_ID']

        key = DataAccess.get_secrets()['PUBG_KEY']
        api = PUBG(key, Shard.STEAM)

        player = list(api.players().filter(player_names=[PUBGname]))[0]
        match = api.matches().get(player.matches[0].id)

        my_roster = None
        for roster in match.rosters:
            am_i_in_this = any([(participant.name == player.name) for participant in roster.participants])
            if am_i_in_this:
                my_roster = roster
                break

        if my_roster:
            idxs = [i if (p.name == player.name) else -1 for i, p in enumerate(my_roster.participants)]
            me = my_roster.participants[max(idxs)]
            squad_names = [p.name for p in my_roster.participants if p.name != player.name]
            print("found roster")
            out = template.format(name = me.name,
                                  damage = int(round(me.damage_dealt, 0)),
                                  numKills = me.kills,
                                  killRank = me.kill_place,
                                  result = me.win_place,
                                  gameType = match.game_mode,
                                  squad="\n".join(squad_names))

            #print(out)
            return out


