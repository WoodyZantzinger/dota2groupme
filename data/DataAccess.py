import json
import os
import pymongo
from data import build_user_from_legacy_data
from data.sUN_user import sUN_user
import time
from pymongo.errors import ConnectionFailure

import json
from bson import ObjectId, json_util


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

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

    def get_x_to_y_map(self, x_key, y_key):
        all_users = self.get_users()
        out = {}
        for user in all_users:
            if not user[y_key]:
                continue
            if user[x_key]:
                if isinstance(user[x_key], list):
                    for (i, val) in enumerate(user[x_key]):
                        out[val] = user[y_key]
                else:
                    out[user[x_key]] = user[y_key]
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

    def get_response_storage(self, clazz, field_name):
        response_data_collection = self.sUN['response_data']
        response_storage = response_data_collection.find_one({"response_name": clazz})
        if response_storage is None or field_name not in response_storage:
            return None
        return response_storage[field_name]

    def set_response_storage(self, clazz, field_name, field_value):
        response_data_collection = self.sUN['response_data']
        query = {"response_name": clazz}
        response_storage = response_data_collection.find_one(query)
        if response_storage is None:
            response_storage = {"response_name": clazz, field_name: field_value}
        response_storage[field_name] = field_value

        response_data_collection.replace_one(query, response_storage, upsert=True)

        pass

    def get_collection_names(self):
        return self.sUN.list_collection_names()

    def get_document_names(self, collection_name):
        coll = self.sUN[collection_name]
        docs = coll.find({})
        return [str(doc) for doc in docs]

    def get_document_item(self, collection_name, doc_idx):
        coll = self.sUN[collection_name]
        docs = coll.find({})
        doc = docs[int(doc_idx)]
        parsed = json.loads(json_util.dumps(doc))
        rval = json.dumps(parsed, indent=4, sort_keys=True)
        return rval

    def set_document_item(self, collection_name, doc_idx, json_str):
        doc_idx = int(doc_idx)
        print(f"collection_name = {collection_name}\ndoc_idx = {doc_idx}\njson_str = {json_str}")
        try:
            json_obj = json_util.loads(json_str)
            coll = self.sUN[collection_name]
            docs = coll.find({})
            doc = docs[doc_idx]
            oid = doc['_id']
            if json_obj['_id'] != oid:
                return False
            for key in json_obj:
                if key == "_id":
                    continue
                doc[key] = json_obj[key]
            coll.replace_one({"_id":oid}, doc, upsert=True)
        except Exception as e:
            print(e)
            return False
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