# -*- coding: utf-8 -*
from AbstractResponse import *
from CooldownResponse import *
import requests
import datetime
import plivo

def get_groupme_token():
    try:
        with open('local_variables.json') as f:
            local_var = json.load(f)
        return local_var["GROUPME_AUTH"]
    except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
        return os.getenv('GROUPME_AUTH')
    except:
        return None

def get_plivo_token():
    try:
        with open('local_variables.json') as f:
            local_var = json.load(f)
        return local_var["PLIVO_AUTH"]
    except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
        return os.getenv('PLIVO_AUTH')
    except:
        return None

def get_plivo_auth():
    try:
        with open('local_variables.json') as f:
            local_var = json.load(f)
        return local_var["PLIVO_AUTH_TOKEN"]
    except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
        return os.getenv('PLIVO_AUTH_TOKEN')
    except:
        return None

class ping(ResponseCooldown):

    message = "#ping"

    RESPONSE_KEY = "#ping"

    COOLDOWN = 1 * 60 * 60 * 3 / 2

    url = 'https://api.groupme.com/v3/groups/13203822?token={token}'

    def __init__(self, msg):
        super(ping, self).__init__(msg, self.__module__, ping.COOLDOWN)

    def respond(self):
        if self.is_sender_off_cooldown():
            user = self.msg.text.partition(' ')[2]
            request_url = ping.url.format(term=get_groupme_token())
            response = requests.get(request_url)
            try:
                print request_url
                for user in response.json()["response"]["members"]:
                    if user["nickname"] == user.lower() and user["muted"]:
                        phone_number = AbstractResponse.Numbers[user["user_id"]]
                        text = "Your ass is being requested in the GroupMe by "

                        message_params = {
                              'src':13306807989,
                              'dst':phone_number,
                              'text':text,
                            }
                        p = plivo.RestAPI(get_plivo_auth(), get_plivo_token())
                        p.send_message(message_params)
                        out = "Ping sent to " + user.lower()

            except Exception:
                out = "Something went wrong"
            self.note_response(out)
            return out
        else:
            print("not responding to ping because sender {} is on cooldown".format(self.sender))
