# -*- coding: utf-8 -*
from .AbstractResponse import *
import sys
import time
from utils import cachedmessage
from dota2py import data

USAGE_MEMBER_NAME = "usage_history"


def get_hero_id(msg_name):
    if len(data.HEROES_CACHE) < 1:
        data.load_heroes()

    matches = []

    for key in data.HEROES_CACHE.items():
        ratio = difflib.SequenceMatcher(None, msg_name.lower(), key[1]['localized_name'].lower()).ratio()
        if ratio > .7:
            matches.append([key, ratio])

    if len(matches) < 1:
        return -1
    else:
        return sorted(matches, key=lambda x: x[1], reverse=True)[0][0][0]


class DotaStatisticsResponse(AbstractResponse):
    usage = {}

    def __init__(self, msg='', obj=None):
        if obj is None:
            obj = self
        super(DotaStatisticsResponse, self).__init__(msg, obj)

    def has_dotaMatch(self, ID):
        ds = DotaStatisticsResponse()
        matches = ds.get_response_storage('matches')
        if not matches:
            return False
        in_storage = [match['match_id'] == ID for match in matches]
        return any(in_storage)

    def add_dotaMatch(self, match):
        ds = DotaStatisticsResponse()
        trimmed_match = {'match_id': match['match_id']}
        matches = ds.get_response_storage('matches')
        if not matches:
            matches = []
        matches.append(trimmed_match)
        ds.set_response_storage('matches', matches)

    def get_record(self, hero_id):
        ds = DotaStatisticsResponse()
        hero_records = ds.get_response_storage('hero_records')
        if not hero_records:
            return None
        downselect = [hero_records[record] for record in hero_records if hero_records[record]['hero_id'] == str(hero_id)]
        if len(downselect):
            return downselect[0]
        else:
            return None

    def get_last_update_time(self):
        ds = DotaStatisticsResponse()
        last_update = ds.get_response_storage('last_update')
        if not last_update:
            return 0
        else:
            return last_update

    def set_last_update_time(self, time):
        ds = DotaStatisticsResponse()
        ds.set_response_storage('last_update', time)

    def set_record(self, hero_id, record):
        ds = DotaStatisticsResponse()
        hero_records = ds.get_response_storage('hero_records')
        if not hero_records:
            hero_records = dict()
        hero_records[str(hero_id)] = record
        ds.set_response_storage('hero_records', hero_records)
