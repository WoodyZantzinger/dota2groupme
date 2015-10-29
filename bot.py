import os
import urllib2
import urllib
import time
import threading
import sys
from flask import Flask, request
from responses import *
import difflib
from responses import AbstractResponse
from utils import rawmessage
from utils import GroupMeMessage
import json
import datetime
import pymongo
import traceback

dummyAR = AbstractResponse.AbstractResponse(None)

DEBUG = False

app = Flask(__name__)

#have the bot do a specific msg in the background constantly (Time in seconds)
def repeat_task(msg, time):
    try:
        #have the bot do a specific msg in the background constantly
        print "Running Repeat Task: " + msg
        active_response_categories = get_response_categories(msg, "sUN-self")
        output_messages = make_responses(active_response_categories, msg, "sUN-self")

        for output in output_messages:
            if output:
                if output != "":
                    send_message(output)
        threading.Timer(time, repeat_task, [msg, time]).start()
    except:
        print("repeat task failed: {}".format(msg))

def send_message(msg, send=True):
    print "Sending: '" + msg + "'"
    if not DEBUG and send:
        url = 'https://api.groupme.com/v3/bots/post'
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        header = {'User-Agent': user_agent, 'Content-Type': 'application/json'}
        values = GroupMeMessage.parse_message(msg)
        req = urllib2.Request(url, json.dumps(values), header)
        response = urllib2.urlopen(req)
        #print "msg"
        return response
    else:
        return 'Win'


def get_response_categories(msg):
    if (msg.sender_id == dummyAR.GroupMeIDs["sUN"]):
        return None
    out = []
    classes = []
    for cls in AbstractResponse.AbstractResponse.__subclasses__():
        classes.append(cls)
    for cls in classes:
        for cls2 in cls.__subclasses__():
            if cls2 not in classes:
                classes.append(cls2)
    for cls in classes:
        if cls.is_relevant_msg(msg):
            print(cls)
            if cls.ENABLED:
                out.append(cls)
            else:
                print("ignoring cls {} because cls is disabled".format(cls))
    if not out:
        return out
    critical_override_threshold = max([cls.OVERRIDE_PRIORITY for cls in out])
    filtered_out = []
    for cls in out:
        if cls.OVERRIDE_PRIORITY >= critical_override_threshold:
            filtered_out.append(cls)
    return filtered_out


def make_responses(categories, msg):
    out = []
    for cls in categories:
        print("sending msg for {}".format(cls))
        out.append(cls(msg).respond())
    return out


@app.route('/message/', methods=['POST'])
def message():
    new_message = request.get_json(force=True)
    msg = rawmessage.RawMessage(new_message)
    print("received message: ")
    print(new_message)
    #sender = new_message["name"]
    #msg = new_message["text"]
    active_response_categories = get_response_categories(msg)
    output_messages = make_responses(active_response_categories, msg)

    # sleep for a second before sending message
    # makes sure that the message from the bot arrives after the message from the user
    time.sleep(1)
    for output in output_messages:
        if output:
            send_message(output)

    return 'OK'

@app.route('/debugmessage/', methods=['POST'])
def debug_message():
    new_message = request.get_json(force=True)
    msg = rawmessage.RawMessage(new_message)
    print("received message: ")
    print(new_message)
    #sender = new_message["name"]
    #msg = new_message["text"]
    active_response_categories = get_response_categories(msg)
    output_messages = make_responses(active_response_categories, msg)

    # sleep for a second before sending message
    # makes sure that the message from the bot arrives after the message from the user
    time.sleep(1)
    for output in output_messages:
        if output:
            send_message(output, send=False)

    return 'OK'


@app.route("/cooldown")
def cooldown():
    response = ""
    for cls in CooldownResponse.ResponseCooldown.__subclasses__():
        if cls.__module__ in sys.modules:
            if hasattr(sys.modules[cls.__module__], 'last_used') and hasattr(cls, "COOLDOWN"):
                response += "<h2>" + cls.__module__ + "</h2>"
                last_time = getattr(sys.modules[cls.__module__], 'last_used')
                for name in last_time:
                    elapsed_time = time.time() - last_time[name]
                    seconds = (elapsed_time - cls.COOLDOWN) * -1
                    if seconds > 0:
                        m, s = divmod(seconds, 60)
                        h, m = divmod(m, 60)
                        time_left = "%d:%02d:%02d" % (h, m, s)
                        response += "Cooldown Remaining for <b>" + name + "</b>: " + time_left + "<br>"
    return response

@app.route("/strava_token")
def strava():
    print "1"
    GroupmeID = request.args.get('state')
    code = request.args.get('code')
    url = 'https://www.strava.com/oauth/token'
    values = {
          'client_id' : '7477',
          'client_secret' : auth_strava.get_strava_key(),
          'code' : code
    }
    print auth_strava.get_strava_key()
    strava_data = urllib.urlencode(values)
    strava_req = urllib2.Request(url, strava_data)
    strava_response = urllib2.urlopen(strava_req)
    StravaData = json.load(strava_response)
    print StravaData
    StravaData['GroupmeID'] = GroupmeID
    conn_start_time = time.time()
    print "1"
    conn = pymongo.Connection(auth_strava.get_db_url())
    print auth_strava.get_db_url()
    conn_time = time.time() - conn_start_time
    print("took {} seconds to connect to mongo".format(conn_time))
    StravaUsers = conn.dota2bot.strava
    result = StravaUsers.insert(StravaData)
    print result
    return "Success! GroupMe, sUN and Strava are synched"

@app.route("/past_response/<name>")
def past_response(name):
    names = AbstractResponse.AbstractResponse.GroupMetoSteam.keys()
    matches = difflib.get_close_matches(name, names, cutoff=0.2)
    if not len(matches):
        return "Could not match name for given name of {}".format(name)
    match = matches[0]
    groupme_id = AbstractResponse.AbstractResponse.GroupMeIDs[match]

    output = "Responses for: <b>{}</b><br>".format(match)
    for cls in CooldownResponse.ResponseCooldown.__subclasses__():
        if cls.__module__ in sys.modules:
            if hasattr(sys.modules[cls.__module__], 'usage_history') and hasattr(cls, "COOLDOWN"):
                cls_responses = getattr(sys.modules[cls.__module__], 'usage_history')
                if groupme_id in cls_responses.keys():
                    output += "<b>{}</b><br>\n".format(cls)
                    for response in cls_responses[groupme_id]:
                        output += "{}<br>".format(response.web_format())
    return output


@app.route("/remindme")
def remindme_callback():
    try:
        print("callbacking on remindme")
        conn = pymongo.Connection(remindme.get_db_url())
        reminders = conn.mjsunbot.reminders

        now = datetime.datetime.now()
        triggered_messages = []
        for item in conn.mjsunbot.reminders.find():
            if (now > item["time"]):
                triggered_messages.append(item)

        names = AbstractResponse.AbstractResponse.GroupMetoSteam.keys()
        out = []
        for item in triggered_messages:
            for name in names:
                try:
                    if AbstractResponse.AbstractResponse.GroupMeIDs[name] == item['senderid']:
                        out.append("Hey, {}: {}".format(name, item["message"]))
                        break
                except:
                    print("error reverse-looking up name: " + name)
            print("triggering message:")
            print(item)
            reminders.remove(item)
        for msg in out:
            send_message(msg)
        return out.__str__()
    except Exception, e:
        (e)
        print(traceback.format_exc())
        return "remindme failed!ex"


@app.route("/")
def hello():
    return "Hello world!"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "debug":
            DEBUG = True

    print(AbstractResponse.AbstractResponse("", "").GroupMeIDs)
    port = int(os.environ.get("PORT", 5000))
    if not DEBUG:
        app.run(host='0.0.0.0', port=port)
        repeat_task('#update', 60 * 30)  # repeat every half an hour
    else:
        app.run(host='0.0.0.0', port=port, debug=True)
