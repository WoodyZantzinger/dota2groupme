import subprocess
import time
import os
import requests
import json
import pprint

MSG_PROCESS = "[#] {}"
MSG_FAIL = "\[!] {}"
MSG_SUCCEED = "\t[ ] {}"

DUT_URL = "http://localhost:5000/message/"

def begin_server():
    with open(os.devnull, 'w') as FNULL:
        pid = subprocess.Popen(["python", "bot.py", "debug"], stdout=FNULL, stderr=FNULL).pid
        return pid

def end_server(pid):
    with open(os.devnull, 'w') as FNULL:
        subprocess.Popen("taskkill /pid {pid} /F".format(pid=pid), stdout=FNULL, stderr=FNULL)

msg_fmt = None
with open("tests\\message_format.json") as f:
    msg_fmt = json.load(f)

pid = begin_server()
time.sleep(10)

print(MSG_PROCESS.format("Server assumed booted"))

r = requests.post(DUT_URL, msg_fmt)

print(MSG_SUCCEED.format(str(r)))

end_server(pid)

time.sleep(1)

print(MSG_PROCESS.format("Finished!"))
