import requests
import time
import json
from data import DataAccess
import sys
import traceback
import websocket
from websocket import create_connection
import ssl

DEBUG = False
HandshakeRequired = True

def subscribe(clientID):
    # Subscribe to the user
    data = [{
        "channel": "/meta/subscribe",
        "clientId": clientID,
        "subscription": "/user/%s" % userID,
        "id": "2",
        "ext": {
            "access_token": accessToken,
            "timestamp": int(time.time())
        }
    }]
    r = requests.post("https://push.groupme.com/faye", json=data)
    if not r.json()[0]["successful"]: raise Exception("Subscription failed")
    #print(r.json()[0])
    return

def on_message(ws, line):
    print(line)
    message = json.loads(line)

    #I'm usnure if GroupMe will ever send back multiple messages but looping through the list just in case
    for single_message in message:

        #try in-case we get some message format I've never seen
        try:
            message_type = single_message["data"]["type"]
            message_type_token = "Unknown"

            #These are the only 4 types I've ever encountered
            #TODO: Find out what ping means to GroupMe and what we do for that message
            if message_type == "direct_message.create": message_type_token = "DM"
            if message_type == "line.create": message_type_token = "Message"
            if message_type == "like.create": message_type_token = "Like"
            if message_type == "ping": message_type_token = "Ping"

            #Right now we ignore Like messages
            if message_type_token == "Message" or message_type_token == "DM":
                message_data = single_message["data"]["subject"]
                print("Message Recieved: " + message_data["text"])
                message_type_token = "Message"

                #if we launch with DEBUG arg, don't send messages onward
                if not DEBUG:
                    r = requests.post("https://young-fortress-3393.herokuapp.com/message/?type={msg_type}".format(
                        msg_type=message_type_token), json=message_data)
                    #print(r.status_code, r.reason)
            else:
                print("Abnormal Response")
                print(single_message)
        except Exception as e:
            print(message)
            traceback.print_exc()
    return

def handshake():
    # Do a long-polling handshake
    # Copied data from tutorial here: https://dev.groupme.com/tutorials/push
    data = [{
        "channel": "/meta/handshake",
        "version": "1.0",
        "supportedConnectionTypes": ["websocket"],
        "id": "1"
    }]
    r = requests.post("https://push.groupme.com/faye", json=data)
    return r.json()[0]["clientId"]

def on_open(ws):
    #print("We Open")
    c_ID = handshake()
    subscribe(c_ID)

    data = [ {
               "channel" : "/meta/connect",
               "clientId" : c_ID,
               "connectionType" : "websocket",
               "id" : "%d" % numCalls
             } ]
    print(data)
    ws.send(json.dumps(data))

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("-- Socket Closed --")

if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == "debug": DEBUG = True

    accessToken = DataAccess.get_secrets()["GROUPME_AUTH"]

    #Get our User ID by asking GroupMe who we are
    data = {"access_token": accessToken}
    r = requests.get("https://api.groupme.com/v3/users/me", params=data)
    userID = r.json()["response"]["user_id"]

    numCalls = 3

    if(DEBUG): websocket.enableTrace(True)

    ws = websocket.WebSocketApp("wss://push.groupme.com/faye",
                                on_message = on_message,
                                on_error=on_error,
                                on_close=on_close
                                )

    ws.on_open = on_open
    ws.run_forever()