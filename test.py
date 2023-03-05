import asyncio
import aiohttp


async def get_signal(session):
    """
    При падении цены более чем на 1% от максимальной за последний час,
    функция выкидывает предупреждение.
    """
    _url = 'https://api.binance.com/api/v3/klines?symbol=XRPUSDT&interval=1m&limit=60'
    async with session.get(_url) as response:
        data = await response.json()
        prices = []
        for elem in data:
            prices.append(float(elem[4]))
        max_price = max(prices)
        last_price = prices[-1]
        if (max_price - last_price) > (max_price / 100):
            return (
                'Цена упала ниже 1% от максимальных показателей за последний час.\n'
                f'Максимальная цена: {max_price}.\n'
                f'Текущая цена: {last_price}'
            )


async def get_price(session):
    """Функция возвращает текущую цену выбранной пары."""
    _url = "https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT"
    async with session.get(_url) as response:
        data = await response.json()
        price = float(data['price'])
        return price


async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            coros = [
                get_price(session),
                get_signal(session)
            ]
            for coro in asyncio.as_completed(coros):
                result = await coro
                print(result) if result else None


if __name__ == '__main__':
    asyncio.run(main())
