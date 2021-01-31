import json
import os
import pymongo
from data import build_user_from_legacy_data
from data.sUN_user import sUN_user
import time

class DataAccess():
    def __init__(self):
        secrets = get_secrets()
        self.client = pymongo.MongoClient(secrets['SUNDATA_URL'])
        self.db = self.client['sUN_users']
        self.users = self.db['users']

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

    def update_user(self, user):
        query = {"GROUPME_ID": user.values["GROUPME_ID"]}
        result = self.users.replace_one(query, user.make_db_object(), upsert=True)
        return result

def store_token(clazz, id, token):
    if 'expires_at' not in token:
        expires_at = time.time() + token['expires_in']
        token['expires_at'] = expires_at
    da = DataAccess()
    user = da.get_user("GROUPME_ID", id)
    user.values[clazz.token_key_name()] = token
    da.update_user(user)


def get_secrets():
    secrets = None
    try:
        with open(os.path.join(os.getcwd(), "local_variables.json")) as f:
            secrets = json.load(f)
    except:
        secrets = dict()
        for key in os.environ.keys():
            local_var[key] = os.environ[key]
    return secrets

def get_secret_keys(clazz):
    id_name = clazz.id_key_name()
    key_name = clazz.key_key_name()
    secrets = get_secrets()
    out = [secrets[id_name], secrets[key_name]]
    return out

def get_current_token(clazz, id):
    da = DataAccess()
    user = da.get_user("GROUPME_ID", id)
    token = None
    token_lookup_key = clazz.token_key_name()
    if token_lookup_key in user.values:
        token = user.values[token_lookup_key]
    return token

if __name__ == "__main__":
    access = DataAccess()
    print("[Getting user Kevin]")
    user = access.get_user("Name", "Kevin")
    print(user)

    print("[All Users]")
    users = access.get_users()
    for user in users:
        print(user)