from common.config import COINMARKETCAP_API_KEY, NEWS_API_KEY
import requests


def get_top_10_cryptos():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
    }
    parameters = {
        'start': '1',
        'limit': '10',
        'convert': 'BGN'
    }
    response = requests.get(url, headers=headers, params=parameters)
    response.raise_for_status()
    data = response.json()
    return data['data']

def get_financial_news():
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': NEWS_API_KEY,
        'category': 'business',
        'country': 'us'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        return articles
    else:
        return None
