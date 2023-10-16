import pprint
import urllib
import time
import sys
import logging
import logging.handlers
from optparse import OptionParser
import os
from flask import Flask, render_template, redirect, request, url_for, session
# import flask.ext.login as flask_login
# from flask_login import flask
# from flask.ext.login import LoginManager, UserMixin
from flask_login import LoginManager, UserMixin
import flask_login
import difflib
import json
import datetime
import pymongo
import traceback
import nltk
import requests
from telegram import _bot

from _groupme_interface import groupme_sender
from _telegram_interface import telegram_sender
from responses import oAuth_util, CooldownResponse, remindme
import pdb
from data import DataAccess
import hashlib
from random import randrange

from responses import *
from responses import AbstractResponse
from statistics import *
from statistics import AbstractStatistics
from utils import rawmessage, BaseMessage, output_message
from utils import GroupMeMessage

DEBUG = True

app = Flask(__name__)
app.secret_key = 'key'

login_manager = LoginManager()
login_manager.init_app(app)

users = {'user1': {'pw': 'pass1'},
         'user2': {'pw': 'pass2'},
         'user3': {'pw': 'pass3'}}

logger = logging.getLogger(__name__)

RESPONSES_CACHE = []
STATISTICS_CACHE = []


def set_debug(debug_level):
    global DEBUG
    DEBUG = debug_level
    logger = logging.getLogger(__name__)

    if (debug_level):
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        logging.basicConfig(format='%(levelname)s in %(funcName)s (%(module)s): \t %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(levelname)s in %(funcName)s (%(module)s): \t %(message)s', level=logging.INFO)
        handler = logging.handlers.RotatingFileHandler(
            "LOG_FILE", maxBytes=20, backupCount=5)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)


def send_message(msg, groupID="13203822", send=True):
    try:
        logger.info(u"Sending: '{}".format(msg))
    except Exception as e:
        line_fail = sys.exc_info()[2].tb_lineno
        logger.debug("\tError: {} on line {}".format(repr(e), line_fail))

    key = DataAccess.get_secrets()["GROUPME_AUTH"]
    url = 'https://api.groupme.com/v3/groups/{id}/messages?token={token}'.format(id=groupID, token=key)

    values = GroupMeMessage.parse_message(msg, groupID)

    final_values = {}
    final_values["message"] = values

    if not DEBUG and send:

        r = requests.post(url, json=final_values)
        print(r.status_code, r.reason)
        #     "source_guid": "GUID",
        #     "recipient_id": "20",
        return r.status_code
    else:
        return 'Win'


def send_direct_message(msg, userID=0, send=True):
    if not DEBUG and send:

        key = DataAccess.get_secrets()["GROUPME_AUTH"]
        url = 'https://api.groupme.com/v3/direct_messages?token={token}'.format(token=key)

        values = GroupMeMessage.parse_message(msg, "0")

        final_values = {}
        values["source_guid"] = "GUID"
        values["recipient_id"] = userID
        final_values["direct_message"] = values

        r = requests.post(url, json=final_values)
        print(r.status_code, r.reason)
        return r.status_code
    else:
        return 'Win'


def like_message(convoID, messageID):
    key = DataAccess.get_secrets()["GROUPME_AUTH"]
    url = 'https://api.groupme.com/v3/messages/{conversation_id}/{message_id}/like?token={token}'.format(token=key,
                                                                                                         conversation_id=convoID,
                                                                                                         message_id=messageID)
    r = requests.post(url)
    print(r.status_code, r.reason)
    return r.status_code


@app.route('/statistics')
def do_last_day_message_statistics():
    # get all messages from the last day

    now = datetime.datetime.utcnow()
    td = datetime.timedelta(hours=5)  # DST can go fuck itself
    EST_NOW = now - td
    td = datetime.timedelta(hours=24)
    EST_1_DAY_AGO = EST_NOW - td

    url = 'https://api.groupme.com/v3/groups/13203822/messages'
    found_a_day_ago = False

    secrets = DataAccess.get_secrets()
    key = secrets["GROUPME_AUTH"]
    values = {"token": key}
    req = requests.get(url, params=values)
    response = json.loads(req.text)
    messages = []
    logger.info("\t[ Loading last day's messages ]")
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
    logger.info("\t[ Last day had {} messages ]".format(len(messages)))

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
    logger.info("Loading responses...")
    for cls in AbstractResponse.AbstractResponse.__subclasses__():
        if cls.ENABLED:
            RESPONSES_CACHE.append(cls)
    for cls in RESPONSES_CACHE:
        for cls2 in cls.__subclasses__():
            if cls2 not in RESPONSES_CACHE:
                if cls2.ENABLED:
                    RESPONSES_CACHE.append(cls2)
    logger.info("Loaded {} response classes".format(len(RESPONSES_CACHE)))
    for cls in sorted([str(cls).lower() for cls in RESPONSES_CACHE]):
        logger.info("loaded response class: {}".format(cls))

    for cls in AbstractStatistics.AbstractStatistics.__subclasses__():
        STATISTICS_CACHE.append(cls)

    logger.info("Loaded {} statistic classes".format(len(STATISTICS_CACHE)))
    for cls in sorted([str(cls).lower() for cls in STATISTICS_CACHE]):
        logger.info("loaded statistics class: {}".format(cls))


sUN_user_id = DataAccess.DataAccess().get_user("Name", "sUN").values['GROUPME_ID']


def get_response_categories(msg):
    sender_uid = msg.get_sender_uid()
    if (msg.get_sender_uid() == sUN_user_id):
        return None
    out = []
    #    for cls in AbstractResponse.AbstractResponse.__subclasses__():
    # classes.append(cls)
    # for cls in classes:
    # for cls2 in cls.__subclasses__():
    # if cls2 not in classes:
    # classes.append(cls2)
    for cls in RESPONSES_CACHE:
        try:
            if cls.is_relevant_msg(msg):
                out.append(cls)
        except:
            print("Relevant msg command failed for class = " + str(cls))
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
        logger.info("sending msg for {}".format(cls))
        out.append(cls(msg).respond())
    return out


tg_bot = _bot.Bot(DataAccess.get_secrets()["TELEGRAM_API_KEY"])


def get_sender_service(msg):
    sender_services = {
        BaseMessage.Services.GROUPME.value: (groupme_sender.GroupMeSender, None),
        BaseMessage.Services.TELEGRAM.value: (telegram_sender.TelegramSender, tg_bot),
    }
    service, bot_obj = sender_services[msg.from_service]
    return service(msg, bot=bot_obj, debug=DEBUG)


@app.route('/message/', methods=['POST'])
def message():
    new_message = request.get_json(force=True)
    msg = BaseMessage.make_message(rawmessage.RawMessage(new_message))
    sender = get_sender_service(msg)

    logger.info("Msg: {msg}".format(msg=msg.text))
    active_response_categories = get_response_categories(msg)

    # if (message_type == "DM" or message_type == "Message") and (randrange(0, 100) > 92):
    #    like_message(new_message["group_id"], new_message["id"])

    if active_response_categories:
        output_messages = make_responses(active_response_categories, msg)
        # sleep for a second before sending message
        # makes sure that the message from the bot arrives after the message from the user

        for output in output_messages:
            if type(output) != output_message.OutputMessage:
                output = output_message.OutputMessage(output, output_message.Services.TEXT)

            if output.obj:
                output.execute(sender)
                print(output.obj)
                # send_message(output, new_message["group_id"])
        if output == None:
            return 'WARNING - Response triggered but not sent'
        else:
            return 'OK - Response Sent'
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


@app.route("/oauth_callback")
@app.route("/oauth_callback/")
def oauth_callback():
    code = request.args.get('code')
    state = request.args.get('state')
    if not code:
        print(request.args)
        return "You're already authorized, congrats!"
    parts = state.split("|")
    source_clazz_name = parts[0]
    sender_id = parts[1]
    print(f"Found sender_id = {sender_id}")
    matched_clazz = None
    for clazz in RESPONSES_CACHE:
        if clazz.__name__ == source_clazz_name:
            matched_clazz = clazz
    dummy_msg = rawmessage.RawMessage({"sender_id": sender_id, 'text': ''})
    dummy_msg = BaseMessage.make_message(dummy_msg) # ????4
    clazz_obj = matched_clazz(dummy_msg)
    matched_clazz.exchange_code_for_first_key(code, clazz_obj, sender_id)
    return f"Success, you can now use {matched_clazz.RESPONSE_KEY}"


@app.route("/strava_token")
def strava():
    GroupmeID = request.args.get('state')
    code = request.args.get('code')
    url = 'https://www.strava.com/oauth/token'
    values = {
        'client_id': '60934',
        'client_secret': oAuth_util.get_strava_key(),
        'code': code
    }
    strava_data = urllib.urlencode(values)
    strava_req = urllib.Request(url, strava_data)
    strava_response = urllib.urlopen(strava_req)
    StravaData = json.load(strava_response)
    logger.info(StravaData)
    StravaData['GroupmeID'] = GroupmeID
    conn_start_time = time.time()
    conn = pymongo.MongoClient(oAuth_util.get_db_url())
    conn_time = time.time() - conn_start_time
    logger.info("took {} seconds to connect to mongo".format(conn_time))
    StravaUsers = conn.dota2bot.strava
    result = StravaUsers.insert(StravaData)
    logger.info(result)
    return "Success! GroupMe, sUN and Strava are synched"


@app.route("/spotify_callback")
def spotify():
    GroupmeID = request.args.get('state')
    code = request.args.get('code')

    r = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'client_id': 'f8597c3f9afb4c1f9f0d3e8d5b53d4ae',
        'redirect_uri': 'https://young-fortress-3393.herokuapp.com/spotify_callback',
        'client_secret': oAuth_util.get_spotify_key(),
        'code': code})

    SpotifyData = r.json()
    SpotifyData['GroupmeID'] = GroupmeID

    conn_start_time = time.time()
    conn = pymongo.MongoClient(oAuth_util.get_db_url())
    conn_time = time.time() - conn_start_time
    logger.info("took {} seconds to connect to mongo".format(conn_time))

    SpotifyUsers = conn.dota2bot.spotify
    result = SpotifyUsers.insert(SpotifyData)
    logger.info(result)
    return "Success! GroupMe, sUN and Spotify are synched"


@app.route("/past_response/<name>")
def past_response(name):
    users = DataAccess.DataAccess().get_users()
    people = [user.values['Name'] for user in users]
    matches = difflib.get_close_matches(name, people, cutoff=0.2)
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
        logger.info("callbacking on remindme")
        rm = remindme.ResponseRemindMe(None)
        reminders = rm.get_response_storage("reminders")

        now = datetime.datetime.now()
        triggered_messages = []
        for reminder in reminders:
            if now > reminder["time"]:
                triggered_messages.append(reminder)

        users = DataAccess.DataAccess().get_users()
        people = {user.values['Name']: user.values['GROUPME_ID'] for user in users}
        out = []
        for item in triggered_messages:
            for name in people:
                try:
                    if people[name] == item['senderid']:
                        msg = item["message"].encode('ascii', errors='ignore')
                        send_group = item["groupid"]
                        text = "Hey, {}: {}".format(name, msg)
                        out.append((text, send_group))
                        break
                except Exception as e:
                    traceback.print_exc()
                    logger.warning("error reverse-looking up name: " + name)
            logger.info("triggering message:")
            reminders.remove(item)
        rm.set_response_storage("reminders", reminders)
        pass
        for msg in out:
            text = msg[0]
            group = msg[1]
            send_message(text, groupID=group)
        return out.__str__()
    except Exception as e:
        (e)
        logger.warning(traceback.format_exc())
        return "remindme failed!ex"


@app.route('/gitevent', methods=['POST'])
def git_event():
    new_event = request.get_json(force=True)
    updates_buffer = "I've been updated!\n"
    for commit in new_event["commits"]:
        updates_buffer += "'" + commit["message"] + "' - " + commit["author"]["name"] + "\n"
    send_message(updates_buffer)
    return updates_buffer


@app.route("/")
def hello():
    return render_template('index.html')
    # return "Hello world!"


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    da = DataAccess.DataAccess()
    users = da.get_admins()
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(req):
    print("RLLLL")
    da = DataAccess.DataAccess()
    admins = da.get_admins()
    username = req.form.get('username')
    pw = req.form.get('pw')
    if username not in admins:
        return

    user = User()
    user.id = username

    hashed_entry = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    if hashed_entry == admins[username]:
        return user
    else:
        return None

    return user


@app.route('/login', methods=['GET', 'POST'])
def index():
    da = DataAccess.DataAccess()
    admins = da.get_admins()
    if request.method == 'POST':
        username = request.form.get('username')
        pw = request.form.get('pw')
        if username not in admins:
            return redirect("/home")
        hashed_entry = hashlib.sha256(pw.encode('utf-8')).hexdigest()
        if hashed_entry == admins[username]:
            user = User()
            user.id = username
            flask_login.login_user(user)
            session['user'] = username
            return redirect(url_for('protect'))
    return render_template('login.html')


def format_text_for_textarea(text):
    lines = text.split('\n')
    out_lines = []
    for line in lines:
        out_lines.append(line)
        # out_lines.append(f"<p>{line}</p>")
    return "\n".join(out_lines)


@app.route('/dbupdate', methods=['POST'])
def database_update():
    newjson = request.form['newjson']
    collection_name = request.form['collection_name']
    doc_idx = request.form['doc_idx']

    da = DataAccess.DataAccess()
    success = da.set_document_item(collection_name, doc_idx, newjson)
    print(f"update success = {success}")
    return str(success)


@app.route('/database_management')
@flask_login.login_required
def manage_db():
    collection_name = request.args.get('collection_name')
    doc_idx = request.args.get('doc_idx')
    print(f"collection_name = {collection_name}")
    print(f"doc_idx = {doc_idx}")
    da = DataAccess.DataAccess()
    names = da.get_collection_names()
    if collection_name and doc_idx:
        pass
    if not collection_name and not doc_idx:
        return render_template('database_management.html',
                               collection_name=None,
                               doc_idx=None,
                               link_list=da.get_collection_names()
                               )
    if collection_name and not doc_idx:
        return render_template('database_management.html',
                               collection_name=collection_name,
                               doc_idx=None,
                               link_list=da.get_document_names(collection_name)
                               )
    if collection_name and doc_idx:
        item_json_str = da.get_document_item(collection_name, doc_idx)
        item_json_str = format_text_for_textarea(item_json_str)
        return render_template('database_management.html',
                               collection_name=collection_name,
                               json=item_json_str,
                               doc_idx=doc_idx
                               )


@app.route('/admin_home')
@flask_login.login_required
def protect():
    user = session['user']
    return render_template('admin_home.html', user=user)


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-d", "--debug", action="store_true", dest="debug",
                      help="Set the bot to debug mode")
    parser.add_option("-p", "--production", action="store_false", dest="debug",
                      help="Set the bot to production mode")

    (options, args) = parser.parse_args()

    set_debug(options.debug)

    load_responses()
    nltk.data.path.append(os.getcwd())

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=DEBUG)
