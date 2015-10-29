import os
import urllib2
import urllib
import traceback
import threading
import sys
from flask import Flask, request
from responses import *

DEBUG = False

app = Flask(__name__)

#have the bot do a specific msg in the background constantly (Time in seconds)
def repeat_task(msg, time):
    #have the bot do a specific msg in the background constantly
    print "Running Repeat Task: " + msg
    active_response_categories = get_response_categories(msg, "sUN")
    output_messages = make_responses(active_response_categories, msg, "sUN")

    for output in output_messages:
        if output:
            if output != "":
                send_message(output)
    threading.Timer(time, repeat_task, [msg, time]).start()

def send_message(msg):
    print "Sending: '" + msg + "'"
    if not DEBUG:
        url = 'https://api.groupme.com/v3/bots/post'
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        header = {'User-Agent': user_agent}
        values = {
          'bot_id' : '535cbd947cf38b46a83fa3084f',
          'text' : msg,
        }
        response_data = urllib.urlencode(values)
        req = urllib2.Request(url, response_data, header)
        response = urllib2.urlopen(req)
        #print "msg"
        return response
    else:
        return 'Win'


def get_response_categories(msg, sender):
    out = []
    for cls in AbstractResponse.AbstractResponse.__subclasses__():
        if cls.is_relevant_msg(msg, sender):
            print(cls)
            out.append(cls)
    if not out:
        return out
    critical_override_threshold = max([cls.OVERRIDE_PRIORITY for cls in out])
    filtered_out = []
    for cls in out:
        if cls.OVERRIDE_PRIORITY >= critical_override_threshold:
            filtered_out.append(cls)
    return filtered_out


def make_responses(categories, msg, sender):
    out = []
    for cls in categories:
        print("sending msg for {}".format(cls))
        out.append(cls(msg, sender).respond())
    return out


@app.route('/message/', methods=['POST'])
def message():
    new_message = request.get_json(force=True)
    sender = new_message["name"]
    msg = new_message["text"]
    if sender == "sUN":
        return "OK"
    active_response_categories = get_response_categories(msg, sender)
    output_messages = make_responses(active_response_categories, msg, sender)

    for output in output_messages:
        if output:
            send_message(output)

    return 'OK'


@app.route("/")
def hello():
    return "Hello world!"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "debug":
            DEBUG = True

    port = int(os.environ.get("PORT", 5000))
    repeat_task('#update', 120)
    if not DEBUG:
        app.run(host='0.0.0.0', port=port)
    else:
        app.run(host='0.0.0.0', port=port, debug=True)