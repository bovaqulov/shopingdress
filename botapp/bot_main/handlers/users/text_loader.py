from telebot.types import Message

from botapp.bot_main.loader import bot
from botapp.bot_main.keyboards import get_btn
from turn_on.models import Category, Product


@bot.message_handler(commands=['start'])
def reaction_start(message: Message):
    chat_id = message.chat.id
    lst = Category.objects.filter(parent=None)
    bot.send_message(chat_id, 'Salom', reply_markup=get_btn([item.title for item in lst]))


@bot.message_handler(func=lambda message: message.text in [item.title for item in Category.objects.filter(parent=None)])
def reaction_category(message: Message):
    chat_id = message.chat.id
    category_title = message.text
    category = Category.objects.get(title=category_title)
    lst = Category.objects.filter(parent=category)
    bot.send_message(chat_id, category_title, reply_markup=get_btn([item.title for item in lst]))

@bot.message_handler(func=lambda message: message.text in [item.title for item in Category.objects.filter(parent=True)])
def reaction_subcategory(message: Message):
    chat_id = message.chat.id
    category_title = message.text
    products_list = Product.objects.filter(category=Category.objects.get(title=category_title))
    bot.send_message(chat_id, category_title, reply_markup=get_btn([item.title for item in products_list]))
