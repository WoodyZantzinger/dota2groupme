import urllib2
import urllib
import time
import sys
from flask import Flask, request
import difflib
from responses import AbstractResponse
from statistics import *
from statistics import AbstractStatistics

from utils import rawmessage
from utils import GroupMeMessage
import json
import datetime
import pymongo
import traceback
import nltk
import requests

DEBUG = False

app = Flask(__name__)

RESPONSES_CACHE = []
STATISTICS_CACHE = []

def send_message(msg, groupID="13203822", send=True):
    try:
        print(u"Sending: '{}".format(msg))
    except Exception, e:
        line_fail = sys.exc_info()[2].tb_lineno
        print("\tError: {} on line {}".format(repr(e), line_fail))
    if not DEBUG and send:
        url = 'https://api.groupme.com/v3/bots/post'
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        header = {'User-Agent': user_agent, 'Content-Type': 'application/json'}
        values = GroupMeMessage.parse_message(msg, groupID)
        req = urllib2.Request(url, json.dumps(values), header)
        response = urllib2.urlopen(req)
        #print "msg"
        return response
    else:
        return 'Win'

@app.route('/statistics')
def do_last_day_message_statistics():
    # get all messages from the last day

    now = datetime.datetime.utcnow()
    td = datetime.timedelta(hours=5) #DST can go fuck itself
    EST_NOW = now - td
    td = datetime.timedelta(hours=24)
    EST_1_DAY_AGO = EST_NOW - td

    url = 'https://api.groupme.com/v3/groups/13203822/messages'
    found_a_day_ago = False
    key = AbstractResponse.AbstractResponse.local_var["GROUPME_AUTH"]
    values = {"token": key}
    req = requests.get(url, params=values)
    response = json.loads(req.text)
    messages = []
    print("\t[ Loading last day's messages ]")
    while not found_a_day_ago:
        for item in response["response"]["messages"]:
            parsed_msg = rawmessage.RawMessage(item)
            messages.append(parsed_msg)
            if datetime.datetime.fromtimestamp(parsed_msg.created_at) < EST_1_DAY_AGO:
                found_a_day_ago = True
                break
        values = {"token": key, "before_id": messages[-1].id}
        req = requests.get(url, params=values)
        response = json.loads(req.text)
    # run all the statistics
    print("\t[ Last day had {} messages ]".format(len(messages)))

    out_message = ""
    print(len(STATISTICS_CACHE))
    for statistic in STATISTICS_CACHE:
        instance = statistic(messages)
        resp = instance.respond()
        if resp:
            print(resp)
            out_message = out_message + resp + "\n"
    send_message(out_message)
    return out_message


def load_responses():
    print("Loading responses...")
    for cls in AbstractResponse.AbstractResponse.__subclasses__():
        if cls.ENABLED:
            RESPONSES_CACHE.append(cls)
    for cls in RESPONSES_CACHE:
        for cls2 in cls.__subclasses__():
            if cls2 not in RESPONSES_CACHE:
                if cls2.ENABLED:
                    RESPONSES_CACHE.append(cls2)
    print("Loaded {} response classes".format(len(RESPONSES_CACHE)))
    for cls in sorted([str(cls).lower() for cls in RESPONSES_CACHE]):
        print("loaded response class: {}".format(cls))

    for cls in AbstractStatistics.AbstractStatistics.__subclasses__():
        STATISTICS_CACHE.append(cls)

    print("Loaded {} statistic classes".format(len(STATISTICS_CACHE)))
    for cls in sorted([str(cls).lower() for cls in STATISTICS_CACHE]):
        print("loaded statistics class: {}".format(cls))


def get_response_categories(msg):
    if (AbstractResponse.AbstractResponse.GroupMeIDs["sUN"]):
        return None
    out = []
#    for cls in AbstractResponse.AbstractResponse.__subclasses__():
        #classes.append(cls)
    #for cls in classes:
        #for cls2 in cls.__subclasses__():
            #if cls2 not in classes:
                #classes.append(cls2)
    for cls in RESPONSES_CACHE:
        if cls.is_relevant_msg(msg):
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

    groupID = new_message["group_id"]

    active_response_categories = get_response_categories(msg)
    if active_response_categories:
        output_messages = make_responses(active_response_categories, msg)
        # sleep for a second before sending message
        # makes sure that the message from the bot arrives after the message from the user
        time.sleep(1)
        for output in output_messages:
            if output:
                send_message(output, groupID)
        return 'OK - Respon se Sent'
    else:
        return 'No Response'


@app.route('/debugmessage/', methods=['POST'])
def debug_message():
    new_message = request.get_json(force=True)
    msg = rawmessage.RawMessage(new_message)
    print("received message: ")
    print(new_message)

    groupID = new_message["group_id"]

    active_response_categories = get_response_categories(msg)
    output_messages = make_responses(active_response_categories, msg)

    # sleep for a second before sending message
    # makes sure that the message from the bot arrives after the message from the user
    time.sleep(1)
    for output in output_messages:
        if output:
            send_message(output, groupID, send=False)

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
    GroupmeID = request.args.get('state')
    code = request.args.get('code')
    url = 'https://www.strava.com/oauth/token'
    values = {
          'client_id': '7477',
          'client_secret': oAuth_util.get_strava_key(),
          'code': code
    }
    strava_data = urllib.urlencode(values)
    strava_req = urllib2.Request(url, strava_data)
    strava_response = urllib2.urlopen(strava_req)
    StravaData = json.load(strava_response)
    print StravaData
    StravaData['GroupmeID'] = GroupmeID
    conn_start_time = time.time()
    print "1"
    conn = pymongo.MongoClient(oAuth_util.get_db_url())
    print oAuth_util.get_db_url()
    conn_time = time.time() - conn_start_time
    print("took {} seconds to connect to mongo".format(conn_time))
    StravaUsers = conn.dota2bot.strava
    result = StravaUsers.insert(StravaData)
    print result
    return "Success! GroupMe, sUN and Strava are synched"

@app.route("/spotify_callback")
def spotify():
    GroupmeID = request.args.get('state')
    code = request.args.get('code')

    r = requests.post('https://accounts.spotify.com/api/token', data = {
        'grant_type':'authorization_code',
        'client_id':'f8597c3f9afb4c1f9f0d3e8d5b53d4ae',
        'redirect_uri':'https://young-fortress-3393.herokuapp.com/spotify_callback',
        'client_secret': oAuth_util.get_spotify_key(),
        'code': code})


    SpotifyData = r.json()
    SpotifyData['GroupmeID'] = GroupmeID

    conn_start_time = time.time()
    conn = pymongo.MongoClient(oAuth_util.get_db_url())
    conn_time = time.time() - conn_start_time
    print("took {} seconds to connect to mongo".format(conn_time))

    SpotifyUsers = conn.dota2bot.spotify
    result = SpotifyUsers.insert(SpotifyData)
    print result
    return "Success! GroupMe, sUN and Spotify are synched"


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
        conn = pymongo.MongoClient(remindme.get_db_url(), connectTimeoutMS=1000)
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
                        msg = item["message"].encode('ascii', errors='ignore')
                        out.append("Hey, {}: {}".format(name, msg))
                        break
                except:
                    print("error reverse-looking up name: " + name)
            print("triggering message:")
            reminders.remove(item)
        for msg in out:
            send_message(msg)
        return out.__str__()
    except Exception, e:
        (e)
        print(traceback.format_exc())
        return "remindme failed!ex"


@app.route('/gitevent', methods=['POST'])
def git_event():
    new_event = request.get_json(force=True)
    updates_buffer = "I've been updated!\n"
    for commit in new_event["commits"]:
        updates_buffer += "'" + commit["message"] + "' - " + commit["author"]["name"] + "\n"
    send_message(updates_buffer, "0")
    return updates_buffer


@app.route("/")
def hello():
    return "Hello world!"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "debug":
            DEBUG = True
    load_responses()
    nltk.data.path.append(os.getcwd())
    print(AbstractResponse.AbstractResponse("", "").GroupMeIDs)
    port = int(os.environ.get("PORT", 5000))
    if not DEBUG:
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        app.run(host='0.0.0.0', port=port, debug=True)
