import requests
import time
import json

# Get new messages from the server
def getNew(c_ID, numCalls):
    # Copied data from tutorial here: https://dev.groupme.com/tutorials/push
    data = [ {
               "channel" : "/meta/connect",
               "clientId" : c_ID,
               "connectionType" : "in-process",
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
        print(message)
        message_data = message[1]["data"]["subject"]
        r = requests.post("http://localhost:5000/message/", json=message_data)
        print(r.status_code, r.reason)
        return

accessToken = "thgXWwUGUtKsk7bpCdISBvubz4zXzgwnsrz5qeU1"
userID = "91085088"

data = {"access_token": accessToken}
r = requests.get("https://api.groupme.com/v3/users/me", params=data)
print(r.json()["response"]["user_id"])

# Copied data from tutorial here: https://dev.groupme.com/tutorials/push
data = [{
    "channel": "/meta/handshake",
    "version": "1.0",
    "supportedConnectionTypes": ["long-polling"],
    "id": "1"
}]
r = requests.post("https://push.groupme.com/faye", json=data)

clientId = r.json()[0]["clientId"]
print(clientId)

# Copied data from tutorial here: https://dev.groupme.com/tutorials/push
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

numCalls = 3
while True:
    getNew(clientId, numCalls)
    numCalls += 1

