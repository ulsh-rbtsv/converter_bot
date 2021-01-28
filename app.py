import telebot
from config import keys, TOKEN
from utils import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Введите валюту в следующем формате (через пробел): \n<имя конвертируемой валюты>' \
'<в какую валюту конвертировать>' \
'<количество конвертируемой валюты>. \n\n' \
'Чтобы увидеть список доступных валют, используйте команду /values.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    quote, base, amount = values

    if len(values) != 3:
        raise ConvertionException('Невозможно обработать такое число параметров')

    total_base = CurrencyConverter.convert(quote, base, amount)

    text = f'{amount} {keys[quote]} ({quote}) = {total_base} {keys[base]} ({base})'
    bot.send_message(message.chat.id, text)


bot.polling()