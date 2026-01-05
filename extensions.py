# extensions.py
import requests
import json

# Словарь доступных валют (ключ — код, значение — читаемое имя)
currency_codes = {
    'USD': 'Доллар США',
    'EUR': 'Евро',
    'RUB': 'Российский рубль'
}

# Обратный словарь: читаемое имя -> код (для поиска при вводе)
currency_names_to_code = {v.lower(): k for k, v in currency_codes.items()}

class APIException(Exception):
    """Исключение для ошибок пользователя"""
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> float:
        """
        Возвращает сумму в валюте quote за amount единиц валюты base.
        Все аргументы — строки.
        """
        base_lower = base.lower()
        quote_lower = quote.lower()

        base_code = None
        quote_code = None

        if base_upper := base.upper():
            if base_upper in currency_codes:
                base_code = base_upper
        if not base_code and base_lower in currency_names_to_code:
            base_code = currency_names_to_code[base_lower]

        if quote_upper := quote.upper():
            if quote_upper in currency_codes:
                quote_code = quote_upper
        if not quote_code and quote_lower in currency_names_to_code:
            quote_code = currency_names_to_code[quote_lower]

        if not base_code:
            raise APIException(f'Не удалось обработать валюту "{base}".')
        if not quote_code:
            raise APIException(f'Не удалось обработать валюту "{quote}".')
        if base_code == quote_code:
            raise APIException('Невозможно перевести одинаковые валюты.')

        try:
            amount_float = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}".')

        if amount_float <= 0:
            raise APIException('Количество должно быть больше 0.')

        url = f'https://api.exchangerate-api.com/v4/latest/{base_code}'
        response = requests.get(url)
        if response.status_code != 200:
            raise APIException('Не удалось получить данные от сервера курсов.')

        data = json.loads(response.text)
        if quote_code not in data['rates']:
            raise APIException(f'Валюта "{quote}" недоступна для конвертации из "{base}".')

        rate = data['rates'][quote_code]
        result = rate * amount_float
        return result