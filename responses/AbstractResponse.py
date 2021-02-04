import json
import os
import pymongo
from dota2py import data
import time
import sys
import difflib


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

    print(f"working directory = {os.getcwd()}")

    with open('./responses/GroupMetoSteam.json') as f:
        GroupMetoSteam = json.load(f)

    with open('./responses/GroupMetoDOTA.json') as f:
        GroupMetoDOTA = json.load(f)

    with open('./responses/GroupMetoXbox.json') as f:
        GroupMetoXbox = json.load(f)

    with open('./responses/GroupMetoLastfm.json') as f:
        GroupMetoLastfm = json.load(f)

    with open('./responses/GroupMetoPUBG.json') as f:
        GroupMetoPUBGName = json.load(f)

    with open('./responses/GroupMetoXboxName.json') as f:
        GroupMetoXboxName = json.load(f)

    with open('./responses/GroupMetoCODName.json') as f:
        GroupMetoCODName = json.load(f)

    with open('./responses/DiscordIDToName.json') as f:
        DiscordIDToName = json.load(f)

    with open('./utils/GroupMeIDs.json') as f:
        GroupMeIDs = json.load(f)

    mongo_connection = None
    """
        try:
            with open('local_variables.json') as f:
                local_var = json.load(f)
            print(local_var["MONGOLAB_URL"])
            conn_start_time = time.time()
            mongo_connection = pymongo.MongoClient(local_var["MONGOLAB_URL"], connectTimeoutMS=1000)
            conn_time = time.time() - conn_start_time
            print("took {} seconds to connect to mongo".format(conn_time))
        except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
            local_var = dict()
            for key in os.environ.keys():
                local_var[key] = os.environ[key]
            conn_start_time = time.time()
            mongo_connection = None
            try:
                print("trying...")
                mongo_connection = pymongo.MongoClient(os.getenv('MONGOLAB_URL'), connectTimeoutMS=1000)
            except Exception as e:
                print("connection to remote db using os.getenv failed!")
                print(e)
            if mongo_connection is not None:
                conn_time = time.time() - conn_start_time
                print("took {} seconds to connect to mongo".format(conn_time))
        except:
            print("failed to connect to mongodb!")
    """

    if mongo_connection:
        mongo_db = mongo_connection.dota2bot
    else:
        mongo_db = None

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
    def get_last_match(cls, name):
        return False

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

    def __init__(self, msg, obj):
        super(AbstractResponse, self).__init__()
        self.clazzname = obj.__class__.__name__
        self.msg = msg

    # def get_last_used_time(self, sender, mod=None):
    #     if mod is not None:
    #         return getattr(sys.modules[mod], 'last_used')[sender]
    #
    # def set_last_used_time(self, sender, mod=None):
    #     if mod is not None:
    #         getattr(sys.modules[mod], 'last_used')[sender] = time.time()

    def respond(self):
        return None

    @classmethod
    def is_relevant_msg(cls, msg):
        return cls.RESPONSE_KEY in msg.text.lower()
