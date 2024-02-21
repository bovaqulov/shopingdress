from telebot import TeleBot

import os

TOKEN = os.getenv("BOT_TOKEN")

bot = TeleBot(TOKEN)