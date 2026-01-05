# bot.py
import telebot
from config import TELEGRAM_BOT_TOKEN
from extensions import CurrencyConverter, APIException, currency_codes

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_help(message):
    text = (
        "Чтобы получить цену валюты, отправьте сообщение в формате:\n"
        "<имя валюты> <в какую валюту перевести> <количество>\n\n"
        "Пример: евро доллар 100\n"
        "Поддерживаются: доллар, евро, рубль (можно использовать коды: USD, EUR, RUB)."
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def send_values(message):
    text = "Доступные валюты:\n" + "\n".join(f"- {name} ({code})" for code, name in currency_codes.items())
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            raise APIException("Неверное количество параметров. Нужно 3: валюта1 валюта2 количество.")

        base, quote, amount = parts
        result = CurrencyConverter.get_price(base, quote, amount)
        bot.reply_to(
            message,
            f"{amount} {base} = {result:.2f} {quote}"
        )
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")

if __name__ == '__main__':
    bot.polling(none_stop=True)