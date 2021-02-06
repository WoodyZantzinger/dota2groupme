import json
import os
import pymongo
from dota2py import data
import time
import sys
import difflib

from data import DataAccess


class AbstractResponse(object):
    # default response key
    # should respond to no messages
    RESPONSE_KEY = "\0"

    # priority of message overriding other messsages
    # to allow some things to make others not come through the pipe
    OVERRIDE_PRIORITY = 0

    ENABLED = True

    # default help response
    HELP_RESPONSE = "Not implemented for " + RESPONSE_KEY


    # TODO work dota statistics classes into a subclass and move these into there
    #   this will be a big pain
    @classmethod
    def has_dotaMatch(cls, ID):
        matches = AbstractResponse.mongo_db.dota2matches
        temp = matches.find_one({'match_id': ID})
        return temp is not None

    @classmethod
    def add_dotaMatch(cls, match):
        matches = AbstractResponse.mongo_db.dota2matches
        matches.insert(match)
        return True

    @classmethod
    def get_record(cls, hero_id):
        records = AbstractResponse.mongo_db.dota2hero_records
        temp = records.find_one({'hero_id': hero_id})
        return temp

    @classmethod
    def get_last_update_time(cls):
        fdata = AbstractResponse.mongo_db.sUN_data
        temp = fdata.find_one()
        return temp

    @classmethod
    def set_last_update_time(cls, time):
        fdata = AbstractResponse.mongo_db.sUN_data
        if '_id' in time:
            fdata.update({'_id': time["_id"]}, {"$set": time}, upsert=True)
            print("Inserted (Update): " + str(time['last_update']))
        else:
            fdata.insert(time)
            print("Inserted (New): " + str(time['last_update']))
        return True

    @classmethod
    def set_record(cls, record):
        records = AbstractResponse.mongo_db.dota2hero_records
        if '_id' in record:
            records.update({'_id': record["_id"]}, {"$set": record}, upsert=True)
        else:
            records.insert(record)
        return True

    @classmethod
    def name_to_dotaID(cls, name):
        return int(AbstractResponse.GroupMetoDOTA[name])

    @classmethod
    def dotaID_to_name(cls, id):
        for name, key in AbstractResponse.GroupMetoDOTA.items():
            if key == id:
                return name

    @classmethod
    def get_hero_id(cls, msg_name):
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

    @classmethod
    def has_dotaID(cls, name):
        return name in AbstractResponse.GroupMetoDOTA

    @classmethod
    def has_dotaID_num(cls, int):
        return int in AbstractResponse.GroupMetoDOTA.values()

    @classmethod
    def has_steamID(cls, name):
        return name in AbstractResponse.GroupMetoSteam

    @classmethod
    def name_to_steamID(cls, name):
        return int(AbstractResponse.GroupMetoSteam[name])

    def __init__(self, msg, obj=None):
        super(AbstractResponse, self).__init__()
        if not obj:
            self.clazzname = None
        else:
            self.clazzname = obj.__class__.__name__
        self.msg = msg

    def respond(self):
        return self._respond()

    def _respond(self):
        return None

    def get_response_storage(self, key):
        if not self.clazzname:
            return None
        da = DataAccess.DataAccess()
        return da.get_response_storage(self.clazzname, key)

    def set_response_storage(self, key, value):
        if not self.clazzname:
            return None
        da = DataAccess.DataAccess()
        da.set_response_storage(self.clazzname, key, value)
    @classmethod
    def is_relevant_msg(cls, msg):
        return cls.RESPONSE_KEY in msg.text.lower()
