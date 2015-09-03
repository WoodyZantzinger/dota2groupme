import requests
import sys

__author__ = 'woodyzantzinger'

request_url = "https://api.groupme.com/v3/groups/13203822/messages?token=xde396cxXkwCQjn2BZQiVojW9XLYd4NxIiYepwwx&limit=100"

if(len(sys.argv) < 2):
    print "You need to specify a UserID"
else:
    user_id = sys.argv[1]
    messages_counted = 0
    response = requests.get(request_url)

    if(len(sys.argv) > 2):
        total_messages = int(sys.argv[2])
    else:
        total_messages = int(response.json()["response"]["count"])

    after_id = -1
    while(messages_counted < total_messages):

        messages = ""

        if after_id < 0:
            response = requests.get(request_url)
            messages = response.json()["response"]["messages"]
        else:
            response = requests.get(request_url + "&before_id=" + after_id)
            messages = response.json()["response"]["messages"]

        for message in messages:
            after_id = message["id"]
            messages_counted = messages_counted + 1
            if message["sender_id"] == user_id:
                try:
                    print message["text"] + "."
                except:
                    pass



