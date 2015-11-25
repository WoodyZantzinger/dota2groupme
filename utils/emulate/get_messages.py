import requests
import sys
import json

__author__ = 'woodyzantzinger'

request_url = "https://api.groupme.com/v3/groups/13203822/messages?token=xde396cxXkwCQjn2BZQiVojW9XLYd4NxIiYepwwx&limit=100"

if(len(sys.argv) < 3):
    print "You need to specify a UserID and output file"
    print "Optional argument for just Text output"
else:
    output_messages = []
    user_id = sys.argv[1]
    messages_counted = 0
    response = requests.get(request_url)

    if(len(sys.argv) > 3):
        total_messages = int(sys.argv[3])
    else:
        total_messages = int(response.json()["response"]["count"])

    after_id = -1
    print total_messages
    while(messages_counted < total_messages):

        messages = ""

        if after_id < 0:
            response = requests.get(request_url)
            messages = response.json()["response"]["messages"]
        else:
            response = requests.get(request_url + "&before_id=" + after_id)
            try:
                messages = response.json()["response"]["messages"]
            except ValueError:
                # We must be done!
                with open(sys.argv[2], 'w') as outfile:
                    json.dump(output_messages, outfile)
                    print "Number of messages: " + str(len(output_messages))
                    break;


        for message in messages:
            after_id = message["id"]
            messages_counted = messages_counted + 1
            if (int(user_id) == 0 or message["sender_id"] == user_id): #and message["sender_id"] != "219313":
                try:
                    output_messages.append(message)
                    #print message["text"]
                except:
                    pass



