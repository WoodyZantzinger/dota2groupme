import json
import os
import pymongo
from data import build_user_from_legacy_data
from data.sUN_user import sUN_user
import time
from pymongo.errors import ConnectionFailure

class DataAccess():
    __client = None

    def __init__(self):
        secrets = get_secrets()
        if DataAccess.__client is None:
            try:
                DataAccess.__client = pymongo.MongoClient(secrets['SUNDATA_URL'])
            except ConnectionFailure as cf:
                DataAccess.__client = None
        if DataAccess.__client:
            self.sUN = DataAccess.__client['sUN_users']
            self.users = self.sUN['users']
            self.admin = self.sUN['admin']

    def get_users(self):
        users_list = list(self.users.find({}))
        users_found = []
        for user in users_list:
            users_found.append(sUN_user(user))
        return users_found

    def get_user(self, key, value):
        search_key = { key: value }
        found = self.users.find_one(search_key)
        if not found:
            return found
        else:
            return sUN_user(found)

    def get_admins(self):
        admins = list(self.admin.find({}))
        out = {}
        for admin in admins:
            out[admin['username']] = admin['hashedpw']
        return out

    def update_user(self, user):
        query = {"GROUPME_ID": user.values["GROUPME_ID"]}
        result = self.users.replace_one(query, user.make_db_object(), upsert=True)
        return result

    def store_token(self, clazz, id, token):
        if 'expires_at' not in token:
            expires_at = time.time() + token['expires_in']
            token['expires_at'] = expires_at

        user = self.get_user("GROUPME_ID", id)
        user.values[clazz.token_key_name()] = token
        self.update_user(user)

    def get_current_token(self, clazz, id):
        user = self.get_user("GROUPME_ID", id)
        token = None
        token_lookup_key = clazz.token_key_name()
        if token_lookup_key in user.values:
            token = user.values[token_lookup_key]
        return token

def get_secrets():
    secrets = None
    try:
        with open(os.path.join(os.getcwd(), "local_variables.json")) as f:
            secrets = json.load(f)
    except EnvironmentError:
        secrets = dict()
        for key in os.environ.keys():
            secrets[key] = os.environ[key]
    return secrets

def get_secret_keys(clazz):
    id_name = clazz.id_key_name()
    key_name = clazz.key_key_name()
    secrets = get_secrets()
    out = [secrets[id_name], secrets[key_name]]
    return out



if __name__ == "__main__":
    access = DataAccess()
    #print("[Getting user Kevin]")
    user = access.get_user("Name", "Kevin")
    #print(user)

    print(access.get_admins())

    #print("[All Users]")
    users = access.get_users()
    for user in users:
        pass
        #print(user)