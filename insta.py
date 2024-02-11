import os
import sys
import telegram
import time
from telegram.ext import Updater, CommandHandler, CallbackContext
import Instaloader
def start(update: telegram.Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Instagram Profile Downloader Bot!")
    def download_profile(update: telegram.Update, context: CallbackContext):
    
    # Get the username from the message
    username = update.message.text.split(' ')[1]

    # Create a new Instaloader object
    L = Instaloader.Instaloader()

    # Download the profile
    try:
        profile = L.load_profile(username)
    except Instaloader.ProfileNotExistsException:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"The profile {username} does not exist.")
        return

    # Download the profile picture
    L.download_profile(profile, profile.username)

    # Download the posts
    for post in profile.get_posts():
        L.download_post(post, target=profile.username)

    # Download the followers
    for follower in profile.get_followers():
        L.download_profile(follower, follower.username)

    # Download the followings
    for following in profile.get_followees():
        L.download_profile(following, following.username)

    # Send a success message
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"The profile {username} has been downloaded.")
    def main():
    # Create a new Telegram bot object
    updater = Updater(token='6919124574:AAGfZ5-2Czv1vqeTlqjgxaiGxvJ83BEsdag', use_context=True)

    # Create a new dispatcher object
    dispatcher = updater.dispatcher

    # Add the start command
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Add the download\_profile command
    download_profile_handler = CommandHandler('download_profile', download_profile)
    dispatcher.add_handler(download_profile_handler)

    # Start the bot
    updater.start_polling()

    # Run the bot forever
    updater.idle()

# Run the main function
if __name__ == '__main__':
    main()