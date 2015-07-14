# -*- coding: utf-8 -*
from AbstractResponse import *
from CooldownResponse import *
import parsedatetime
import pymongo
import datetime

print("connection to reminders DB established")

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
        return os.getenv('MONGOLAB_URL')
    except:
        return None

class ResponseRemindMe(ResponseCooldown):

    RESPONSE_KEY = "#remindme"

    COOLDOWN = 1

    def __init__(self, msg):
        super(ResponseRemindMe, self).__init__(msg, self.__module__, ResponseRemindMe.COOLDOWN)

    def respond(self):
        conn = pymongo.Connection(get_db_url())
        reminders = conn.mjsunbot.reminders

        for item in reminders.find():
            print(item)

        if self.is_sender_off_cooldown():
            now = time_parser.parse("now")
            if (self.msg.text.split(" ")[0].lower() != "#remindme"):
                return
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
                    else:
                        print("time is before now, not sending")
                else:
                    print("couldn't find second quot")
            else:
                print("couldn't find first quot")
        else:
            print("not responding to #what because sender {} is on cooldown".format(self.msg.name))