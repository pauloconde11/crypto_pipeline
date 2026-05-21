import requests
from dotenv import load_dotenv
import os

load_dotenv()

COIN_GECKO_API_KEY = os.getenv("COIN_GECKO_API_KEY")

SYMBOL_MAPPING = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "litecoin": "LTC",
}

def fetch_market_data():
    try:

        url = "https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=bitcoin,ethereum&names=Bitcoin,Ethereum&symbols=btc,eth&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true"

        headers = {"x-cg-demo-api-key": COIN_GECKO_API_KEY}

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            raw_data = response.json()
            crypto_data = []
            for coin_id, coin_data in raw_data.items():
                formatted_coin = {
                    "symbol": SYMBOL_MAPPING[coin_id],
                    "price": coin_data.get("usd"),
                    "market_cap": coin_data.get("usd_market_cap"),
                    "volume_24h": coin_data.get("usd_24h_vol"),
                    "change_24h": coin_data.get("usd_24h_change"),
                    "currency": "USD",
                    "timestamp": coin_data.get("last_updated_at")
                }
                crypto_data.append(formatted_coin)
            return crypto_data
        else:
            print("Error fetching market data")
    except Exception as e:
        print(f"Error fetching market data: {e}")
        return None

market_data = fetch_market_data()
print(market_data)
