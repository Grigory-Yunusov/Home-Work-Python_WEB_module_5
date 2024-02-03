import aiohttp
import asyncio
import json
from datetime import datetime, timedelta


class ExchangeRateAPI:
    API_URL = "https://api.privatbank.ua/#p24/exchangeArchive"

    async def get_exchange_rates(self, start_date, end_date):
        if (end_date - start_date).days > 10:
            print("Помилка: Можна запитати курс валют не більше, ніж за останні 10 днів.")
            return

        params = {
            "json": "",
            "date": end_date.strftime("%d.%m.%Y")
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.API_URL, params=params) as response:
                    data = await response.json()
                    if response.status != 200 or "exchangeRate" not in data:
                        print("Помилка: Неможливо отримати курс валют.")
                        return

                    exchange_rates = data["exchangeRate"]
                    result = {}

                    for rate in exchange_rates:
                        if rate["currency"] in ["EUR", "USD"]:
                            result[rate["currency"]] = rate["saleRateNB"]

                    return result

            except aiohttp.ClientError as e:
                print(f"Помилка мережі: {e}")

def main():
    start_date = datetime.now() - timedelta(days=10)
    end_date = datetime.now()

    api = ExchangeRateAPI()
    loop = asyncio.get_event_loop()
    exchange_rates = loop.run_until_complete(api.get_exchange_rates(start_date, end_date))

    if exchange_rates:
        print(f"Курс EUR: {exchange_rates.get('EUR')}")
        print(f"Курс USD: {exchange_rates.get('USD')}")

if __name__ == "__main__":
    main()