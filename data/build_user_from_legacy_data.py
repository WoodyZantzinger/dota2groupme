import json
from collections import defaultdict
import pprint

# groupmeID -->utils/GroupMeIDs.json
# steam ID
# discord ID
# CODName
# PUBG
# xbox id
# xbox name
from data.sUN_user import sUN_user


def add_to_model_from_json(model, username, newkey, jsonpath):
    with open(jsonpath) as f:
        data = defaultdict(lambda: None, json.load(f))
        model[newkey] = data[username]
    return model

def build_legacy_user_objects():
    GMID_data = None
    with open("../utils/GroupMeIDs.json") as f:
        GMID_data = json.load(f)

    print(GMID_data)

    models = []
    for username in GMID_data:
        user_model = dict()
        user_model['Name'] = username

        user_model = add_to_model_from_json(user_model, username, 'DOTA_ID', "../responses/GroupMetoDOTA.json")
        user_model = add_to_model_from_json(user_model, username, 'GROUPME_ID', "../utils/GroupMeIDs.json")
        user_model = add_to_model_from_json(user_model, username, 'STEAM_ID', "../responses/GroupMetoSteam.json")
        user_model = add_to_model_from_json(user_model, username, 'PUBG_ID', "../responses/GroupMetoPUBG.json")
        user_model = add_to_model_from_json(user_model, username, 'COD_ID', "../responses/GroupMetoCODName.json")

        models.append(user_model)

    for model in models:
        user = sUN_user(model)
        print(user)

    return models

if __name__ == "__main__":
    models = build_legacy_user_objects()