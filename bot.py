import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from roombapy import Roomba
from functools import wraps

from content.creds import ROOMBA_IP, ROOMBA_BLID, ROOMBA_PASSWORD, TELEGRAM_TOKEN, AUTHORIZED_USER_ID

# Replace these values with your own

# Initialize Roomba API
roomba = Roomba(address=ROOMBA_IP, blid=ROOMBA_BLID, password=ROOMBA_PASSWORD, continuous=True)
roomba.connect()


def restricted(func):
    @wraps(func)
    def wrapped(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != AUTHORIZED_USER_ID:
            update.message.reply_text("Unauthorized access. You are not allowed to use this bot.")
            return
        return func(update, context, *args, **kwargs)

    return wrapped


def get_room_id(room_name):
    # You need to create a mapping between room names and region_ids
    from content.cleaning_config import room_mapping
    return room_mapping.get(room_name.lower())


def args(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        args = context.args
        return func(update, context, *args, **kwargs)

    return wrapped


@restricted
@args
def clean_room(update: Update, context: CallbackContext, *args):
    if len(args) == 1:
        room_name = args[0]
        room_id = get_room_id(room_name)

        if room_id:
            map_id = "YOUR_MAP_ID"  # Replace this with your actual map_id
            roomba.send_command("start_room", map_id=map_id, region_ids=[room_id])
            update.message.reply_text(f"Starting to clean {room_name}...")
        else:
            update.message.reply_text(f"Could not find the room")


@restricted
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr"Hi {user.mention_markdown_v2()}\!",
        reply_markup=ForceReply(selective=True),
    )


@restricted
def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("Available commands:\n"
                              "/start\n"
                              "/help\n"
                              "/start_clean\n"
                              "/clean_room {Room Name}\n"
                              "/stop_clean")


@restricted
def start_clean(update: Update, context: CallbackContext):
    roomba.send_command("start")
    update.message.reply_text("Starting the iRobot...")


@restricted
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
    dispatcher.add_handler(CommandHandler("clean_room", clean_room))

    # Start the bot
    updater.start_polling()

    # Run the bot until it's stopped
    updater.idle()


if __name__ == "__main__":
    main()
