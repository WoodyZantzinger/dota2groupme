import datetime
import logging

import requests
import os

import sys
sys.path.append("..")

print(os.getcwd())
from telegram import __version__ as TG_VER, ForceReply

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import time
import json


from data import DataAccess
from utils import BaseMessage

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

"""
{
  "attachments": [],
  "avatar_url": "https://i.groupme.com/123456789",
  "created_at": 1302623328,
  "group_id": "1234567890",
  "id": "11111",
  "name": "MALDICIÓN",
  "sender_id": "113",
  "sender_type": "user",
  "source_guid": "GUID",
  "system": false,
  "text": "#gif Sample Gif",
  "user_id": "1112121"
}
"""


def serialize_update(obj):  # this method can go straight to hell, I will never understand it again
    try:
        if type(obj) == list and obj:
            out = []
            for _ in obj:
                upd = serialize_update(_)
                if upd:
                    out.append(upd)
            return out
    except:
        pass

    try:
        if (not obj) or (not hasattr(obj, "__slots__")):
            return obj
        else:
            out = {}
            attr_names = [o for o in dir(obj) if not o.startswith("_")]
            for k in attr_names:
                attr = getattr(obj, k)
                if callable(attr) or k.startswith("_"):
                    continue
                sud = serialize_update(attr)
                if type(sud) == datetime.datetime:
                    sud = time.mktime(sud.timetuple())
                if sud:
                    out[k] = sud
            return out
    except Exception as e:
        print(obj)
        raise e

def reformat_telegram_message(update: Update):
    send_text = ""
    if update.message.text:
        send_text = update.message.text
    if update.message.caption:
        send_text = update.message.caption

    reformat = {
        "attachments": [],
        "avatar_url": "",
        "created_at": int(time.mktime(update.message.date.timetuple())),
        "group_id": update.message.chat_id,
        "id": -1,
        "name": update.message.from_user.name,
        "sender_id": update.message.from_user.id,
        "source_guid": "GUID",
        "system": False,
        "text": send_text,
        "user_id": update.message.from_user.id,
        "from_service": BaseMessage.Services.TELEGRAM.value,
    }

    other_data = serialize_update(update)
    reformat.update(other_data)

    return reformat

async def command_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("found command!")
    text = update.message.text + " as a command"
    print(text)

async def plaintext_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("echoing" + update.message.text)
    json = reformat_telegram_message(update)
    #bm = BaseMessage.make_message(json)
    # fnames = await bm.save_attachments_to_local(context.bot)
    # bm.get_sender_uid()
    if update.message.chat.type == "private":
        #out = "Your ID is: " + str(bm.raw_msg['sender_id'])
        #await context.bot.send_message(chat_id=update.effective_chat.id, text=out)
        #return
        pass
    url_debug = "http://localhost:5000/message/?type={msg_type}"
    url_live = "https://young-fortress-3393.herokuapp.com/message/?type={msg_type}"
    r = requests.post(url_live.format(
        msg_type="Message"), json=json)
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=json['text'])

def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    secrets = DataAccess.get_secrets()
    telegram_api_key = secrets["TELEGRAM_API_KEY"]
    application = Application.builder().token(telegram_api_key).build()

    # on different commands - answer in Telegram

    # on non command i.e message - echo the message on Telegram
    unknown_handler = MessageHandler(filters.COMMAND, command_callback)
    application.add_handler(unknown_handler)

    plaintext_handler = MessageHandler((filters.CAPTION | filters.ATTACHMENT | filters.TEXT) & (~filters.COMMAND), plaintext_callback)
    application.add_handler(plaintext_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()