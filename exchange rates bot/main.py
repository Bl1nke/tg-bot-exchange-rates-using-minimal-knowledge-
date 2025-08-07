import requests
from config import TOKEN
from telebot import *
import json

bot = telebot.TeleBot(TOKEN)

url_currencies_of_countries = "https://www.cbr-xml-daily.ru/daily_json.js"

api_key_for_crypto = 	"CG-BsZfKwM3koaTdrzdZAjxrEVg"
url_currencies_of_crypto = "https://api.coingecko.com/api/v3/simple/price"

params = {
    "ids": "bitcoin,ethereum,tether",
    "vs_currencies": "usd,eur"
}

headers = {
    "x-cg-demo-api-key": api_key_for_crypto  # или "x-cg-pro-api-key"
}

response_currencies_of_crypto = requests.get(url_currencies_of_crypto, params=params, headers=headers)
data_currencies_of_crypto = response_currencies_of_crypto.json()
bitcoin_rate = data_currencies_of_crypto["bitcoin"]["usd"]
ethereum_rate = data_currencies_of_crypto["ethereum"]["usd"]
tether_rate = data_currencies_of_crypto["tether"]["usd"]



response_currencies_of_countries = requests.get(url_currencies_of_countries)
data_currencies_of_countries = response_currencies_of_countries.json()
usd_rate = data_currencies_of_countries["Valute"]["USD"]["Value"]
eur_rate = data_currencies_of_countries["Valute"]["EUR"]["Value"]
gbp_rate = data_currencies_of_countries["Valute"]["GBP"]["Value"]
aed_rate = data_currencies_of_countries["Valute"]["AED"]["Value"]
cny_rate = data_currencies_of_countries["Valute"]["CNY"]["Value"]
pln_rate = data_currencies_of_countries["Valute"]["PLN"]["Value"]
try_rate = data_currencies_of_countries["Valute"]["TRY"]["Value"]

@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    currencies_of_countries = types.KeyboardButton("🏦 Валюты стран")
    currencies_of_crypto = types.KeyboardButton("🪙 Криптовалюты")


    markup.add(currencies_of_countries, currencies_of_crypto)

    bot.send_message(message.chat.id, "Здравствуй, {0.first_name}! Выбери то, что хочешь поменять сегодня.".format(message.from_user), reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "🏦 Валюты стран")
def handle_countries(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    usd_rate_button = types.KeyboardButton("🍔 Доллар США")
    eur_rate_button = types.KeyboardButton("🏰 Евро")
    gpb_rate_button = types.KeyboardButton("💂 Фунты Стерлинга")
    aed_rate_button = types.KeyboardButton("🏎️ Дирхам")
    cny_rate_button = types.KeyboardButton("🐲 Юань")
    pln_rate_button = types.KeyboardButton("🇵🇱 Злота")
    try_rate_button = types.KeyboardButton("🇹🇷 Лира")
    Go_back_button = types.KeyboardButton('🔙 Назад')

    markup.add(usd_rate_button, eur_rate_button, 
            gpb_rate_button, aed_rate_button,
            cny_rate_button, try_rate_button,
            pln_rate_button,
            Go_back_button)
    

    bot.send_message(
        message.chat.id,
        "Выберете желаемую валюту", 
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "🍔 Доллар США")
def handle_countries(message):
    bot.send_message(message.chat.id, f"Доллар США: {usd_rate} рублей")

@bot.message_handler(func=lambda message: message.text == "🏰 Евро")
def handle_countries(message):
    bot.send_message(message.chat.id, f"Евро: {eur_rate} рублей")

@bot.message_handler(func=lambda message: message.text == "💂 Фунты Стерлинга")
def handle_countries(message):
    bot.send_message(message.chat.id, f"Фунты Стерлинга: {gbp_rate} рублей")

@bot.message_handler(func=lambda message: message.text == "🏎️ Дирхам")
def handle_countries(message):
    bot.send_message(message.chat.id, f"Дирхам: {aed_rate} рублей")

@bot.message_handler(func=lambda message: message.text == "🐲 Юань")
def handle_countries(message):
    bot.send_message(message.chat.id, f"Юань: {cny_rate} рублей")

@bot.message_handler(func=lambda message: message.text == "🇵🇱 Злота")
def handle_countries(message):
    bot.send_message(message.chat.id, f"Злота: {pln_rate} рублей")

@bot.message_handler(func=lambda message: message.text == "🇹🇷 Лира")
def handle_countries(message):
    bot.send_message(message.chat.id, f"Лира: {try_rate} рублей")

@bot.message_handler(func=lambda message: message.text == '🔙 Назад')
def handle_back(message):
    send_welcome(message)



@bot.message_handler(func=lambda message: message.text == "🪙 Криптовалюты")
def handle_crypto(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bitcoin_rate_button = types.KeyboardButton("₿ Биткойн")
    ethereum_rate_button = types.KeyboardButton("ETH Эфир")
    tether_rate_button = types.KeyboardButton("TET Тедер")
    Go_back_button = types.KeyboardButton('🔙 Назад')


    markup.add(bitcoin_rate_button, ethereum_rate_button, tether_rate_button, Go_back_button)

    bot.send_message(
        message.chat.id,
        "Выберете желаемую криптовалюту", 
        reply_markup=markup
    )



@bot.message_handler(func=lambda message: message.text == "₿ Биткойн")
def handle_countries(message):
    bot.send_message(message.chat.id, f"Биткойн: {bitcoin_rate} Долларов")

@bot.message_handler(func=lambda message: message.text == "TET Тедер")
def handle_countries(message):
    bot.send_message(message.chat.id, f"Тедер: {tether_rate} Долларов")

@bot.message_handler(func=lambda message: message.text == "ETH Эфир")
def handle_countries(message):
    bot.send_message(message.chat.id, f"Эфир: {ethereum_rate} Долларов")






if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            def send_error(message):
                bot.send_message(message.chat.id, "Бот больше, не работает")