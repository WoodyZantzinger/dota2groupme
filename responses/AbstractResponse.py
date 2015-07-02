import json
import os
import pymongo
from dota2py import data
import time
import sys

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

    with open('./responses/GroupMetoSteam.json') as f:
        GroupMetoSteam = json.load(f)

    with open('./responses/GroupMetoDOTA.json') as f:
        GroupMetoDOTA = json.load(f)

    with open('./utils/GroupMeIDs.json') as f:
        GroupMeIDs = json.load(f)

    key = "63760574A669369C2117EA4A30A4768B"


    mongo_connection = None

    try:
        with open('local_variables.json') as f:
            local_var = json.load(f)
        print local_var["MONGOLAB_URL"]
        conn_start_time = time.time()
        mongo_connection = pymongo.Connection(local_var["MONGOLAB_URL"])
        conn_time = time.time() - conn_start_time
        print("took {} seconds to connect to mongo".format(conn_time))
    except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
        conn_start_time = time.time()
        mongo_connection = pymongo.Connection(os.getenv('MONGOLAB_URL'))
        conn_time = time.time() - conn_start_time
        print("took {} seconds to connect to mongo".format(conn_time))
    except:
        print("failed to connect to mongodb!")

    if mongo_connection:
        mongo_db = mongo_connection.dota2bot
    else:
        mongo_db = None

    @classmethod
    def has_dotaMatch(cls, ID):
        matches = AbstractResponse.mongo_db.dota2matches
        temp = matches.find_one({'match_id': ID})
        return (temp is not None)

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
        data = AbstractResponse.mongo_db.sUN_data
        temp = data.find_one()
        return temp

    @classmethod
    def set_last_update_time(cls, time):
        data = AbstractResponse.mongo_db.sUN_data
        if time.has_key('_id'):
            data.update({'_id': time["_id"]}, {"$set": time}, upsert=True)
            print "Inserted (Update): " + str(time['last_update'])
        else:
            data.insert(time)
            print "Inserted (New): " + str(time['last_update'])
        return True

    @classmethod
    def set_record(cls, record):
        records = AbstractResponse.mongo_db.dota2hero_records
        if record.has_key('_id'):
            records.update({'_id': record["_id"]}, {"$set": record}, upsert=True)
        else:
            records.insert(record)
        return True

    @classmethod
    def get_last_match(cls, name):
        return False

    @classmethod
    def name_to_dotaID(cls, name):
        return int(AbstractResponse.GroupMetoDOTA[name])

    #TODO: We need to optimize, this is a poor was to do reverse lookups
    @classmethod
    def dotaID_to_name(cls, id):
        for name, key in AbstractResponse.GroupMetoDOTA.items():
            if key == id:
                return name

    @classmethod
    def get_hero_id(cls, msg_name):
        if len(data.HEROES_CACHE) < 1:
            data.load_heroes()

        for key in data.HEROES_CACHE.items():
            if msg_name.lower() == (key[1]['localized_name'].lower()):
                return key[0]

    @classmethod
    def has_dotaID(cls, name):
        return AbstractResponse.GroupMetoDOTA.has_key(name)

    @classmethod
    def has_dotaID_num(cls, int):
        return int in AbstractResponse.GroupMetoDOTA.values()

    @classmethod
    def has_steamID(cls, name):
        return AbstractResponse.GroupMetoSteam.has_key(name)

    @classmethod
    def name_to_steamID(cls, name):
        return int(AbstractResponse.GroupMetoSteam[name])

    @classmethod
    def cache_GroupMetoSteam(cls):
        with open('./responses/GroupMetoSteam.json', 'w') as f:
            json.dump(AbstractResponse.GroupMetoSteam, f)

    @classmethod
    def cache_GroupMetoDOTA(cls):
        with open('./responses/GroupMetoDOTA.json', 'w') as f:
            json.dump(AbstractResponse.GroupMetoDOTA, f)

    @classmethod
    def update_user(cls, old, new):
        AbstractResponse.GroupMetoSteam[new] = AbstractResponse.GroupMetoSteam[old]
        del AbstractResponse.GroupMetoSteam[old]
        AbstractResponse.cache_GroupMetoSteam()

        AbstractResponse.GroupMetoDOTA[new] = AbstractResponse.GroupMetoDOTA[old]
        del AbstractResponse.GroupMetoDOTA[old]
        AbstractResponse.cache_GroupMetoDOTA()

    def __init__(self, msg, mod=None):
        super(AbstractResponse, self).__init__()
        self.msg = msg

    def get_last_used_time(self, sender, mod=None):
        if mod is not None:
            return getattr(sys.modules[mod], 'last_used')[sender]

    def set_last_used_time(self, sender, mod=None):
        if mod is not None:
            getattr(sys.modules[mod], 'last_used')[sender] = time.time()

    def respond(self):
        return None

    @classmethod
    def is_relevant_msg(cls, msg):
        return cls.RESPONSE_KEY in msg.text.lower()