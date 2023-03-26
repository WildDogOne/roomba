import logging
import requests
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from functools import wraps

from content.creds import TELEGRAM_TOKEN, rest980_host, rest980_port, AUTHORIZED_USER_ID

# Replace with your Roomba's IP and port
ROOMBA_IP = rest980_host
ROOMBA_PORT = rest980_port

# Replace with your Telegram bot API key
TELEGRAM_TOKEN = TELEGRAM_TOKEN

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def restricted(func):
    @wraps(func)
    def wrapped(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != AUTHORIZED_USER_ID:
            update.message.reply_text("Unauthorized access. You are not allowed to use this bot.")
            return
        return func(update, context, *args, **kwargs)

    return wrapped


@restricted
def start(update: Update, _: CallbackContext):
    update.message.reply_text(
        'Hi! I am your Roomba control bot. You can use the following commands:\n/start_clean - Start cleaning\n/stop_clean - Stop cleaning\n/get_status - Get Roomba status')


@restricted
def start_clean(update: Update, _: CallbackContext):
    response = requests.get(f'http://{ROOMBA_IP}:{ROOMBA_PORT}/api/local/action/start')
    if response.status_code == 200:
        update.message.reply_text('Roomba has started cleaning.')
    else:
        update.message.reply_text('Error: Could not start Roomba.')


@restricted
def stop_clean(update: Update, _: CallbackContext):
    response = requests.get(f'http://{ROOMBA_IP}:{ROOMBA_PORT}/api/local/action/stop')
    if response.status_code == 200:
        update.message.reply_text('Roomba has stopped cleaning.')
    else:
        update.message.reply_text('Error: Could not stop Roomba.')


@restricted
def get_status(update: Update, _: CallbackContext):
    response = requests.get(f'http://{ROOMBA_IP}:{ROOMBA_PORT}/api/local/info/state')
    if response.status_code == 200:
        status = response.json()
        update.message.reply_text(f'Roomba status: {status["cleanMissionStatus"]["phase"]}')
    else:
        update.message.reply_text('Error: Could not get Roomba status.')


def main():
    updater = Updater(TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("start_clean", start_clean))
    dispatcher.add_handler(CommandHandler("stop_clean", stop_clean))
    dispatcher.add_handler(CommandHandler("get_status", get_status))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
