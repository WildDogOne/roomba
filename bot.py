import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from roombapy import Roomba

from content.creds import ROOMBA_IP, ROOMBA_BLID, ROOMBA_PASSWORD, TELEGRAM_TOKEN


# Replace these values with your own

# Initialize Roomba API
roomba = Roomba(address=ROOMBA_IP, blid=ROOMBA_BLID, password=ROOMBA_PASSWORD, continuous=True)
roomba.connect()


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr"Hi {user.mention_markdown_v2()}\!",
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("Available commands:\n/start\n/help\n/start_clean\n/stop_clean")


def start_clean(update: Update, context: CallbackContext):
    roomba.send_command("start")
    update.message.reply_text("Starting the iRobot...")


def stop_clean(update: Update, context: CallbackContext):
    roomba.send_command("stop")
    update.message.reply_text("Stopping the iRobot...")


def main():
    # Set up the logging
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )

    # Initialize the Updater with your bot's token
    updater = Updater(TELEGRAM_TOKEN)

    # Register the command handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("start_clean", start_clean))
    dispatcher.add_handler(CommandHandler("stop_clean", stop_clean))

    # Start the bot
    updater.start_polling()

    # Run the bot until it's stopped
    updater.idle()


if __name__ == "__main__":
    main()
