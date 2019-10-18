import json
import os
import pymongo

DB_Key = ""

try:
    with open('local_variables.json') as f:
        local_var = json.load(f)
    DB_Key =  local_var["MONGOLAB_URL"]
except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
    DB_Key = os.getenv('MONGOLAB_URL')
except:
    DB_Key = None

class User:
    def __init__(self):
        self.username = ''
        self.password = ''


def create_user(username, password):

    if DB_Key == None: return False
    mongo_connection = pymongo.MongoClient(local_var["MONGOLAB_URL"], connectTimeoutMS=1000, retryWrites=False)
    mongo_db = mongo_connection.dota2bot

    users = mongo_db.users

    new_user = {'username': username, 'password': password}

    users.insert(new_user)

    return True