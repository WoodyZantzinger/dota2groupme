import requests
import sys
import json
from progressbar import ProgressBar

__author__ = 'woodyzantzinger'

request_url = "https://api.groupme.com/v3/groups/13203822/messages?token=xde396cxXkwCQjn2BZQiVojW9XLYd4NxIiYepwwx&limit=100"

output_to_print = True

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
    pbar = ProgressBar(
        maxval=total_messages,
    )

    pbar.start()
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
                pbar.finish()
                if output_to_print:
                    with open(sys.argv[2], 'w') as outfile:
                        for message in output_messages:
                            if message["text"] is not None:
                                if (message["text"].endswith(".") or
                                    message["text"].endswith("!") or
                                    message["text"].endswith("?") or
                                    message["text"].endswith(". ") or
                                    message["text"].endswith("! ") or
                                    message["text"].endswith("? ")):
                                    outfile.write(message["text"].encode('utf-8') + "\n")
                                else:
                                    outfile.write(message["text"].encode('utf-8') + ".\n")
                        break;
                else:
                    with open(sys.argv[2], 'w') as outfile:
                        json.dump(output_messages, outfile)
                        break;


        for message in messages:
            after_id = message["id"]
            messages_counted = messages_counted + 1
            pbar.update(messages_counted)
            if (int(user_id) == 0 or message["sender_id"] == user_id) and message["sender_id"] != "219313":
                try:
                    output_messages.append(message)
                except:
                    pass
    print "Number of messages: " + str(len(output_messages))




