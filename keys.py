import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import secrets
import json
import os
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Path to store keys
KEYS_FILE = "keys.json"

# Load existing keys
def load_keys():
    if os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, "r") as file:
            return json.load(file)
    return {}

# Save keys to file
def save_keys(keys):
    with open(KEYS_FILE, "w") as file:
        json.dump(keys, file, indent=4)

def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message and bot usage instructions."""
    update.message.reply_text(
        "Welcome! Use /generate_key <hours> to create a time-limited key."
    )

def generate_key(update: Update, context: CallbackContext) -> None:
    """Generate a unique time-limited key."""
    try:
        # Parse duration (in hours) from user command
        duration = int(context.args[0]) if context.args else 24  # Default: 24 hours
        expiration = datetime.now() + timedelta(hours=duration)

        # Generate a secure random key
        key = secrets.token_hex(16)  # 16-byte key (32 characters)

        # Load existing keys and add the new one
        keys = load_keys()
        keys[key] = expiration.strftime("%Y-%m-%d %H:%M:%S")

        # Save the updated keys
        save_keys(keys)

        # Send the key back to the user
        update.message.reply_text(
            f"Generated Key: {key}\nValid for: {duration} hours\nExpires at: {expiration}"
        )
        logger.info(f"Generated Key: {key} (Expires at {expiration})")
    except Exception as e:
        update.message.reply_text("Error: Please provide a valid duration in hours.")
        logger.error(e)

def main():
    """Start the bot."""
    # Your bot token from BotFather
    BOT_TOKEN = "7861057999:AAGkCLAsS8GSWRdrkHw3zuxh30FOXnNhh_w"

    # Create the Updater and pass it your bot's token
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("generate_key", generate_key))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    # Ensure the keys file exists
    if not os.path.exists(KEYS_FILE):
        open(KEYS_FILE, "w").close()
    main()
