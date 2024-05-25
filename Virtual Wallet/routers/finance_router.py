from fastapi import APIRouter, HTTPException, Depends
from services.finance_service import get_top_10_cryptos, get_financial_news
import requests
from common.auth import get_current_active_user
from data_.models import User

finance_router = APIRouter(prefix='/Finance', tags= ['Financial news'])

@finance_router.get('/top10cryptos')
async def top_10_cryptos(current_user: User = Depends(get_current_active_user)):
    try:
        cryptos = get_top_10_cryptos()
        filtered_cryptos = [{ 'name': crypto['name'], 'symbol': crypto['symbol'], 'price': crypto['quote']['USD']['price'] } for crypto in cryptos]
        return filtered_cryptos
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

@finance_router.get('/news')
async def financial_news():
    news = get_financial_news()
    if news:
        return news
    else:
        return {"error": "Failed to fetch financial news"}