# -*- coding: utf-8 -*
import requests

from data import DataAccess
from .AbstractResponse import *
import random


class ResponseValorantLast(AbstractResponse):

    match_performance_template = "You {outcome} as {agent}. You went {k}:{d}:{a}, and rounds went {wins}/{losses}."

    RESPONSE_KEY = "#valorantlast"

    LINK_TEMPLATE = r"https://api.henrikdev.xyz/valorant/v3/matches/{region}/{username}/{tag}"

    def __init__(self, msg):
        super(ResponseValorantLast, self).__init__(msg)

    def _respond(self):

        user = DataAccess.DataAccess().get_user("GROUPME_ID", self.msg.sender_id)
        region = user['RIOT_REGION']
        username = user['RIOT_USERNAME']
        tag = user['RIOT_TAG']
        request_url = ResponseValorantLast.LINK_TEMPLATE.format(region=region, username=username, tag=tag)

        print("Got Account ID")
        # Get a list of recent matches for the player
        matches = json.loads(requests.get(request_url).content)
        last_match = matches['data'][0]
        this_user = [pl for pl in last_match['players']['all_players'] if pl['name']==username][0]
        my_team = this_user['team']
        k = this_user['stats']['kills']
        d = this_user['stats']['deaths']
        a = this_user['stats']['assists']
        agent = this_user['character']

        win_loss = 'tied'
        for team in last_match['teams']:
            if team == my_team and last_match['teams'][team]['has_won']:
                win_loss = 'won'

            if team != my_team and last_match['teams'][team]['has_won']:
                win_loss = 'lost'

        wins = last_match['teams'][my_team.lower()]["rounds_won"]
        losses = last_match['teams'][my_team.lower()]["rounds_lost"]

        res_str = ResponseValorantLast.match_performance_template.format(
            outcome=win_loss,
            agent=agent,
            k=k, d=d, a=a,
            wins=wins, losses=losses
        )

        return res_str
