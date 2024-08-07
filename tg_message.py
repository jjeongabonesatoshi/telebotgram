import os
import telebot
from dotenv import load_dotenv, dotenv_values #a library use to scrape the env.
import time
load_dotenv()
API_KEY = os.getenv("API_KEY") # getting the API_KEY variable from .env
bot = telebot.TeleBot(API_KEY)
chat_id = 7346012683
 #write down my own chat_ID

#
def send_periodic_message():
    bot.send_message(chat_id, "This is a periodic message sent every minute.")
    bot.polling(none_stop=True)
# if __name__ == '__main__':
#     start_bot()