import requests
import time
import json
from data import DataAccess


def getNew(c_ID, numCalls):
    # Copied data from tutorial here: https://dev.groupme.com/tutorials/push
    data = [ {
               "channel" : "/meta/connect",
               "clientId" : c_ID,
               "connectionType" : "long-polling",
               "id" : "%d" % numCalls
             } ]
    try:
        #this is a blocking request. It will hold until there is something to return
        r = requests.post("https://push.groupme.com/faye", json=data, stream=True)
    except requests.exceptions.RequestException as e:
        print("There was a problem getting the next messages.")
        print(e)
        return
    for line in r.iter_lines():
        message = json.loads(line.decode("utf-8"))
        #print(message)
        for single_message in message[1:]:
            message_type = single_message["data"]["type"]
            if message_type == "direct_message.create": message_type_token = "DM"
            if message_type == "line.create": message_type_token = "Message"
            if message_type == "like.create": message_type_token = "Like"
            if message_type == "ping": message_type_token = "Ping"

            if message_type_token != "Ping":
                message_data = single_message["data"]["subject"]
                print(message_data["text"])
                message_type_token = "Message"
                #r = requests.post("http://localhost:5000/message/?type={msg_type}".format(msg_type=message_type_token), json=message_data)
                print(r.status_code, r.reason)
        return

def handshake():
    # Do a long-polling handshake
    # Copied data from tutorial here: https://dev.groupme.com/tutorials/push
    data = [{
        "channel": "/meta/handshake",
        "version": "1.0",
        "supportedConnectionTypes": ["long-polling"],
        "id": "1"
    }]
    r = requests.post("https://push.groupme.com/faye", json=data)
    return r.json()[0]["clientId"]

if __name__ == "__main__":
    accessToken = DataAccess.get_secrets()["GROUPME_AUTH"]

    #Get our User ID by asking GroupMe who we are
    data = {"access_token": accessToken}
    r = requests.get("https://api.groupme.com/v3/users/me", params=data)
    #print(r.json()["response"]["user_id"])
    userID = r.json()["response"]["user_id"]

    clientId = handshake()
    print(clientId)

    # Subscribe to the user
    data = [{
        "channel": "/meta/subscribe",
        "clientId": clientId,
        "subscription": "/user/%s" % userID,
        "id": "2",
        "ext": {
            "access_token": accessToken,
            "timestamp": int(time.time())
        }
    }]
    r = requests.post("https://push.groupme.com/faye", json=data)
    if not r.json()[0]["successful"]: raise Exception("Subscription failed")
    print(r.json()[0])
    numCalls = 3
    while True:
        getNew(clientId, numCalls)
        numCalls += 1
