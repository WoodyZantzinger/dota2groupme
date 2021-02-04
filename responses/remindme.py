# -*- coding: utf-8 -*
from .AbstractResponse import *
from .CooldownResponse import *
import parsedatetime
import pymongo
import datetime

c = parsedatetime.Constants()
c.BirthdayEpoch = 80
time_parser = parsedatetime.Calendar(c)

quot = "\""


def get_db_url():
    try:
        with open('local_variables.json') as f:
            local_var = json.load(f)
        return local_var["REMINDMEURL"]
    except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
        return os.getenv('REMINDMEURL')
    except:
        return None


class ResponseRemindMe(ResponseCooldown):

    RESPONSE_KEY = "#remindme"

    OVERRIDE_PRIORITY = 1

    COOLDOWN = 10 * 60

    def __init__(self, msg):
        super(ResponseRemindMe, self).__init__(msg, self, ResponseRemindMe.COOLDOWN)

    def _respond(self):
        conn = None
        try:
            conn = pymongo.MongoClient(get_db_url(), connectTimeoutMS=1000)
        except:
            print("failed to connect to reminders-db")
            return None

        reminders = conn.mjsunbot.reminders
        print("remindme: connected to db")

        #for item in reminders.find():
        #    print(item)

        if self.is_sender_off_cooldown():
            print("sender is off CD")
            now = time_parser.parse("now")
            if (self.msg.text.split(" ")[0].lower() != "#remindme"):
                return
            print("first word was remindme")
            firstquot = self.msg.text.find(quot)
            if (firstquot != -1):
                secondquot = self.msg.text[firstquot + 1:].find(quot)
                if (secondquot != -1):
                    time = self.msg.text[firstquot + 1:firstquot + 1 + secondquot]
                    time = time_parser.parse(time)
                    if (time > now):
                        body = self.msg.text[firstquot + 1 + secondquot + 1:]
                        dt = datetime.datetime(*time[0][:6])
                        storemsg = {"message": body, "time": dt, "senderid": self.msg.sender_id}
                        reminders.insert(storemsg)
                        print("inserting message: " + str(storemsg))
                        return "I will remind {} about {}. Beep boop.".format(self.msg.name, body)
                    else:
                        print("time is before now, not sending")
                else:
                    print("couldn't find second quot")
            else:
                print("couldn't find first quot")
        else:
            print("not responding to #what because sender {} is on cooldown".format(self.msg.name))
