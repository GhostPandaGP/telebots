from django.core.management.base import BaseCommand

from telebot.models import Messages
from telebot.models import Profile

import logging

from telegram import Bot
from telegram import Update
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.utils.request import Request

from dj_telebot.settings import TG_TOKEN
from dj_telebot.settings import TG_API_URL
from dj_telebot.settings import ADMIN_IDS
from dj_telebot.settings import MAIN_ADMIN_ID


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


button_help = "Помощь"


def log_error(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'[ADMIN] Произошла ошибка {e}'
            logger.error(error_message)

            update = args[0]
            if update and hasattr(update, 'message'):
                for admin in MAIN_ADMIN_ID:
                    update.message.bot.send_message(
                        chat_id=admin,
                        text=error_message,
                    )
            raise e

    return inner


def admin_access(f):

    def inner(*args, **kwargs):
        update = args[0]
        if update and hasattr(update, 'message'):
            chat_id = update.message.chat_id  # 492618436
            if chat_id in ADMIN_IDS:
                logger.info(f"Доступ разрешен по id: {chat_id}")
                return f(*args, **kwargs)
            else:
                logger.info(f"Доступ запрещен по id: {chat_id}")
                return
        else:
            logger.warning("Нет аргумента update")

    return inner


@log_error
def button_help_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Это помощь!',
        reply_markup=ReplyKeyboardRemove(),
    )


@log_error
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )

    m = Messages(
        profile=p,
        text=text,
    )
    m.save()

    text = f"Ваше сообщение: '{update.message.text}' c id: {m.pk}"
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_help),
            ],
        ],
        resize_keyboard=True,
    )

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
    )


@admin_access
@log_error
def secret_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='секрет!',
    )


@admin_access
@log_error
def secret_command2(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='секрет2!',
    )
    sec


@log_error
def count_messages(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    count = Messages.objects.filter(profile=p).count()

    update.message.reply_text(
        text=f'У вас {count} сообщений'
    )


def controller_handler(update: Update, context: CallbackContext):
    logger.info(update.message)

    text = update.message.text
    if text == button_help:
        return button_help_handler(update=update, context=context)
    else:
        do_echo(update=update, context=context)


class Command(BaseCommand):
    help = 'Телеграмм бот'

    def handle(self, *args, **options):
        req = Request(
            connect_timeout=1,
        )
        bot = Bot(
            request=req,
            token=TG_TOKEN,
            base_url=TG_API_URL,
        )
        updater = Updater(
            bot=bot,
            use_context=True,
        )
        logger.info(updater.bot.get_me())

        command1 = CommandHandler('secret', secret_command)
        updater.dispatcher.add_handler(command1)

        command2 = CommandHandler('secret2', secret_command2)
        updater.dispatcher.add_handler(command2)

        command2 = CommandHandler('count', count_messages)
        updater.dispatcher.add_handler(command2)

        message_handler = MessageHandler(filters=Filters.text, callback=controller_handler)
        updater.dispatcher.add_handler(message_handler)

        updater.start_polling()
        updater.idle()
