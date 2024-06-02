# -*- coding: utf-8 -*
import requests

from data import DataAccess
from .AbstractResponse import *
import random


class ResponseValorantLast(AbstractResponse):

    match_performance_template = "You {outcome} as {agent} on {map}. You went {k}:{d}:{a}, and rounds went {wins}/{losses}. Teammates:"

    RESPONSE_KEY = "#valorantlast"

    LINK_TEMPLATE = r"https://api.henrikdev.xyz/valorant/v3/matches/{region}/{username}/{tag}?api_key={api_key}"

    def __init__(self, msg):
        super(ResponseValorantLast, self).__init__(msg)

    def _respond(self):
        valorant_key = DataAccess.get_secrets()["VALORANT_API_KEY"]
        user = DataAccess.DataAccess().get_user("GROUPME_ID", self.msg.get_sender_uid())
        region = user['RIOT_REGION']
        username = user['RIOT_USERNAME']
        tag = user['RIOT_TAG']
        request_url = ResponseValorantLast.LINK_TEMPLATE.format(region=region, username=username, tag=tag, api_key=valorant_key)

        print("Got Account ID")
        # Get a list of recent matches for the player
        matches = json.loads(requests.get(request_url).content)
        last_match = matches['data'][0]
        map = last_match['metadata']['map']
        this_user = [pl for pl in last_match['players']['all_players'] if pl['name']==username][0]
        my_team = this_user['team'].lower()
        k = this_user['stats']['kills']
        d = this_user['stats']['deaths']
        a = this_user['stats']['assists']
        agent = this_user['character']
        teammates = [pl['name'] + "#" + pl['tag'] for pl in last_match['players'][my_team.lower()] if pl['name'] != username]

        win_loss = 'tied'
        for team in last_match['teams']:
            if team == my_team and last_match['teams'][team]['has_won']:
                win_loss = 'won'

            if team != my_team and last_match['teams'][team]['has_won']:
                win_loss = 'lost'

        wins = last_match['teams'][my_team]["rounds_won"]
        losses = last_match['teams'][my_team]["rounds_lost"]

        res_str = ResponseValorantLast.match_performance_template.format(
            outcome=win_loss,
            agent=agent,
            map=map,
            k=k, d=d, a=a,
            wins=wins, losses=losses
        )
        res_str = res_str +"\n\t" + "\n\t".join(teammates)

        return res_str
