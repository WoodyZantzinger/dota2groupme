import os
import urllib2
import urllib
import traceback
import sys
from flask import Flask, request
from responses import *

DEBUG = False

app = Flask(__name__)

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

<<<<<<< HEAD
=======
            #Items?
            finalItems = "Your items: "
            for itemNum in range(0, 6):
                if x["item_" + str(itemNum)] != 0 and x["item_" + str(itemNum)] is not None:
                    finalItems += str(data.get_item_name(x["item_" + str(itemNum)])["name"]) + ", "
            send_message(finalItems)

            #Win?
            if player_num < 5 and match["result"]["radiant_win"]:
                send_message("You Won!")
            elif player_num > 4 and not match["result"]["radiant_win"]:
                send_message("You Won!")
            else:
                send_message("You Lost.... Bitch")
        player_num = player_num + 1
    return 'OK'


def current_online(msg, user):
    return send_message("No one is online!")


def show_help(msg, user):
    send_message("Fuck you " + str(user) + "... This shit isn't that hard")
    for command, help_text in help_dict.iteritems():
        send_message(command + ": " + help_text)
    return 'OK'


def status(msg, user):
    return send_message("Currently listening...")


def nextHero(msg, user):
    return send_message("You will play " + random_hero())


def nextItem(msg, user):
    return send_message("You will buy " + random_item())


def nextTeam(msg, user):
    # makes a list of 5 random heroes
    heroes = [random_hero() for _ in range(5)]
    return send_message(local_data.team_template.format(*heroes))


def send_burn(msg, user):
    return send_message(random.choice(local_data.burn_responses))


def send_insult():
    return send_message("No, you {}".format(random.choice(local_data.mean_names)))

options = {"#last": last_game,
           "#now": current_online,
           "#setsteam": set_steam,
           "#setdota": set_dota,
           "#status": status,
           "#help": show_help,
           "#next": nextHero,
           "#nextitem": nextItem,
           "#nextteam": nextTeam,
           "#sunstrike": send_burn,
}
>>>>>>> master

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
    if not DEBUG:
        app.run(host='0.0.0.0', port=port)
    else:
        app.run(host='0.0.0.0', port=port, debug=True)