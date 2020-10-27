from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from settings import TG_TOKEN
from bs4 import BeautifulSoup
import requests

def sms(bot, update):
    print('Кто-то отправил команду /start. Что мне делать?')
    bot.message.reply_text('Здравствуйте {}! \nПоговорите со мной!'.format(bot.message.chat.first_name), reply_markup = get_keyboard())

def get_anecdote(bot, update):
    receive = requests.get('http://anekdotme.ru/random')
    page = BeautifulSoup(receive.text, "html.parser")
    find = page.select('.anekdot_text')
    for text in find:
        page = (text.getText().strip())
        bot.message.reply_text(page)
def parrot(bot, update):
    print(bot.message.text)
    bot.message.reply_text(bot.message.text)

def get_contact(bot, update):
    print(bot.message.contact)
    bot.message.reply_text('{}, мы получили ваш номер телефона'.format(bot.message.chat.first_name))

def get_location(bot, update):
    print(bot.message.location)
    bot.message.reply_text('{}, мы получили ваше местоположение'.format(bot.message.chat.first_name))


def get_keyboard():
    contact_button = KeyboardButton('Отправить контакты', request_contact=True)
    location_button = KeyboardButton('Отправить геопозицию', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([['Анекдот', 'Начать'],[contact_button, location_button]], resize_keyboard=True)
    return my_keyboard
def main():
    my_bot = Updater(TG_TOKEN, use_context=True)
    my_bot.dispatcher.add_handler(CommandHandler('start', sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Начать'), sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Анекдот'), get_anecdote))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.contact, get_contact))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.location, get_location))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))
    my_bot.start_polling()
    my_bot.idle()


main()
