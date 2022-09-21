import logging

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

import sys
sys.path.append("..")
from data import DataAccess

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("echoing")
    text = update.message.text + " you dumb idiot"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def echoEveryhing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("EE")
    text = update.message.text
    print(text)
    await update.message.reply_text("You said: " + text)


def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    secrets = DataAccess.get_secrets()
    TG_KEY = secrets["TELEGRAM_API_KEY"]
    application = Application.builder().token(TG_KEY).build()

    # on different commands - answer in Telegram
    #application.add_handler(CommandHandler("start", start))
    #application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)
    application.add_handler(MessageHandler(filters.TEXT, echoEveryhing))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()