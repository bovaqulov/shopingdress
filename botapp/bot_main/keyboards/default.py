from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def get_btn(lst:list):
    markup = ReplyKeyboardMarkup(row_width=1)
    for item in lst:
        markup.add(KeyboardButton(item))
    return markup
