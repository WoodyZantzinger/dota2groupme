import logging

from utils import BaseMessage
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

import sys
sys.path.append("..")
from data import DataAccess

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
def reformat_telegram_message(update: Update):
    send_text = ""
    if update.message.text:
        send_text = update.message.text
    if update.message.caption:
        send_text = update.message.caption

    reformat = {
        "attachments": [],
        "avatar_url": "",
        "created_at": time.mktime(update.message.date.timetuple()),
        "group_id": update.message.chat_id,
        "id": -1,
        "name": "",
        "sender_id": update.message.from_user.id,
        "source_guid": "GUID",
        "system": False,
        "text": send_text,
        "user_id": update.message.from_user.id,
        "from_service": BaseMessage.Services.TELEGRAM.value,
    }
    return reformat

async def command_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("found command!")
    text = update.message.text + " as a command"
    print(text)

async def plaintext_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("echoing")
    json = reformat_telegram_message(update)
    print(json)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=json['text'])

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