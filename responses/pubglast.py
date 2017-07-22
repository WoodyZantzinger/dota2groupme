# -*- coding: utf-8 -*
from AbstractResponse import AbstractResponse
import os
import json
from pypubg import core
import time

class ResponsePUBGLast(AbstractResponse):

    RESPONSE_KEY = "#pubglast"

    def __init__(self, msg):
        super(ResponsePUBGLast, self).__init__(msg)

    def respond(self):
        out = ""
        canonical_name = (key for key,value in AbstractResponse.GroupMeIDs.items() if value==self.msg.sender_id).next()

        steamid = AbstractResponse.GroupMetoSteam[canonical_name]

        key = None
        try:
            with open('local_variables.json') as f:
                local_var = json.load(f)
                key = local_var["PUBG_KEY"]
        except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
            key = os.getenv('PUBG_KEY')
        except:
            print "Something went very wrong in #halolast for the Halo key"

        # get player results
        api = core.PUBGAPI(key)
        steamdata = api.player_s(steamid)
        nick = steamdata['Nickname']
        time.sleep(1.5)
        playerdata = api.player(nick)
        lastmatch = playerdata['MatchHistory'][0]

        mode = lastmatch['MatchDisplay']
        rating = lastmatch['Rating']
        delta = lastmatch['RatingChange']
        sign = "+" if delta > 0 else "-"
        delta = abs(delta)
        kills = lastmatch['Kills']
        assists = lastmatch['Assists']
        damage = lastmatch['Damage']
        headshots = lastmatch['Headshots']
        distance = str(lastmatch['MoveDistance'] / 1000) + " km"
        survival_time = lastmatch['TimeSurvived']
        surv_min = int(survival_time // 60)
        surv_sec = int(survival_time - surv_min * 60)
        duration = '{}:{}'.format(surv_min, surv_sec)

        statsfmt = \
"""
Mode: {mode}
Rating: {rating} [{sign}{delta}]
Kills: {kills}
Assists: {assists}
Damage: {damage}
Headshots: {headshots}
Distance: {distance}
Duration: {duration}
"""

        resp = statsfmt.format(
                    mode=mode,
                    rating=rating,
                    sign=sign,
                    delta=delta,
                    kills=kills,
                    assists=assists,
                    damage=damage,
                    headshots=headshots,
                    distance=distance,
                    duration=duration
            )

        winstr = "You won!"
        t10str = "You placed in the top 10!"
        genstr = "You generally sucked."

        top10 = lastmatch['Top10']
        won = lastmatch['Wins']

        resstr = ""
        if won:
            resstr = winstr
        elif top10:
            resstr = t10str
        else:
            resstr = genstr

        out = resstr + '\n~~~~~~~~~~~' + resp

        return out


