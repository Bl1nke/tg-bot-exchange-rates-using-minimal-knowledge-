import requests
from config import TOKEN, API_KEY_CRYPTO, URL_CBR, URL_CRYPTO, CRYPTO_CURRENCIES, FIAT_CURRENCIES
from telebot import types, TeleBot
import logging
from datetime import datetime, timedelta
import time


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


bot = TeleBot(TOKEN)


crypto_data = None
fiat_data = None
last_updated = None


CRYPTO_BUTTONS = {
    "₿ Биткойн": ("bitcoin", "usd"),
    "ETH Эфир": ("ethereum", "usd"),
    "TET Тедер": ("tether", "usd"),
}

FIAT_BUTTONS = {
    "🍔 Доллар США": ("USD", "Value"),
    "🏰 Евро": ("EUR", "Value"),
    "💂 Фунты Стерлинга": ("GBP", "Value"),
    "🏎️ Дирхам": ("AED", "Value"),
    "🐲 Юань": ("CNY", "Value"),
    "🇵🇱 Злота": ("PLN", "Value"),
    "🇹🇷 Лира": ("TRY", "Value"),
}


def fetch_crypto_rates():
    params = {
        "ids": ",".join(CRYPTO_CURRENCIES),
        "vs_currencies": "usd,eur"
    }
    headers = {"x-cg-demo-api-key": API_KEY_CRYPTO}
    
    try:
        response = requests.get(URL_CRYPTO, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе курсов криптовалют: {e}")
        return None

def fetch_fiat_rates():
    try:
        response = requests.get(URL_CBR, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе курсов валют: {e}")
        return None

def update_rates():
    global crypto_data, fiat_data, last_updated
    try:
        crypto_data = fetch_crypto_rates()
        fiat_data = fetch_fiat_rates()
        if crypto_data is None or fiat_data is None:
            raise ValueError("Не удалось получить данные от API")
        last_updated = datetime.now()
        logger.info("Данные о курсах обновлены")
        return True
    except Exception as e:
        logger.error(f"Ошибка при обновлении курсов: {e}")
        return False

def get_rates():
    global last_updated
    if not last_updated or (datetime.now() - last_updated) > timedelta(minutes=5):
        if not update_rates():
            return None, None
    return crypto_data, fiat_data


@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_fiat = types.KeyboardButton("🏦 Валюты стран")
    btn_crypto = types.KeyboardButton("🪙 Криптовалюты")
    markup.add(btn_fiat, btn_crypto)

    bot.send_message(
        message.chat.id,
        f"Здравствуй, {message.from_user.first_name}! Выбери, что тебя интересует:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "🏦 Валюты стран")
def show_fiat_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(text) for text in FIAT_BUTTONS]
    buttons.append(types.KeyboardButton('🔙 Назад'))
    markup.add(*buttons)

    bot.send_message(
        message.chat.id,
        "Выберите валюту:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "🪙 Криптовалюты")
def show_crypto_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(text) for text in CRYPTO_BUTTONS]
    buttons.append(types.KeyboardButton('🔙 Назад'))
    markup.add(*buttons)

    bot.send_message(
        message.chat.id,
        "Выберите криптовалюту:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text in CRYPTO_BUTTONS)
def handle_crypto_currency(message):
    crypto_data, _ = get_rates()
    
    if not crypto_data:
        bot.send_message(message.chat.id, "⚠️ Не удалось получить данные о криптовалютах. Попробуйте позже.")
        return

    crypto, currency = CRYPTO_BUTTONS[message.text]
    try:
        rate = crypto_data[crypto][currency]
        bot.send_message(
            message.chat.id,
            f"{message.text.split()[1]}: {rate} {currency.upper()}"
        )
    except KeyError:
        bot.send_message(message.chat.id, "⚠️ Информация по этой криптовалюте временно недоступна")

@bot.message_handler(func=lambda message: message.text in FIAT_BUTTONS)
def handle_fiat_currency(message):
    _, fiat_data = get_rates()
    
    if not fiat_data:
        bot.send_message(message.chat.id, "⚠️ Не удалось получить данные о валютах. Попробуйте позже.")
        return

    currency, key = FIAT_BUTTONS[message.text]
    try:
        rate = fiat_data["Valute"][currency][key]
        bot.send_message(
            message.chat.id,
            f"{message.text.split()[1]}: {rate} руб."
        )
    except KeyError:
        bot.send_message(message.chat.id, "⚠️ Информация по этой валюте временно недоступна")

@bot.message_handler(func=lambda message: message.text == '🔙 Назад')
def handle_back(message):
    send_welcome(message)


if __name__ == "__main__":
    logger.info("Запуск бота...")
    if not update_rates():
        logger.error("Не удалось получить начальные данные о курсах")

    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logger.error(f"Ошибка в работе бота: {e}", exc_info=True)
            time.sleep(5)