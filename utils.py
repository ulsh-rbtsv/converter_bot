import requests
import json
from config import keys


class ConvertionException(Exception):
    pass


class NegativeAmountException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'Не удалось конвертировать одинаковые валюты "{base}"')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        if amount < 0:
            raise NegativeAmountException(f'Не удалось обработать отрицательное количество {amount}')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?symbols={quote_ticker}&base={base_ticker}')
        total_base = float(amount) / float(json.loads(r.content)['rates'][keys[quote]])

        return round(total_base, 3)

