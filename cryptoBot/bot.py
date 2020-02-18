import logging

from telegram import InlineQueryResultArticle
from telegram import InputTextMessageContent
from telegram import ReplyKeyboardRemove
from telegram import Update
from telegram import Bot
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.ext import Filters
from telegram.ext import CallbackContext
from telegram.ext import InlineQueryHandler

from cryptoBot.config import TG_API_URL
from cryptoBot.config import TG_TOKEN

from 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cryptoBot")


def do_echo(update: Update, context: CallbackContext):
    text = update.message.text
    update.message.reply_text(
        text=text
    )


def main():
    bot = Bot(
        token=TG_TOKEN,
        base_url=TG_API_URL,
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )
    logger.info(updater.bot.get_me())

    message_handler = MessageHandler(Filters.text, do_echo)
    updater.dispatcher.add_handler(message_handler)
    logger.debug("hello world!")

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()