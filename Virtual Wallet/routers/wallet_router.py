from typing import Annotated
from fastapi import APIRouter, Depends

from common.auth import get_current_active_user
from data_.models import User
from services.wallet_service import add_money_to_wallet, withdraw_money_from_wallet, get_wallet_balance

wallet_router = APIRouter(prefix='/wallets', tags=["Wallet"])


@wallet_router.get("/balance")
async def get_balance(
    current_user: Annotated[User, Depends(get_current_active_user)]):
    balance = get_wallet_balance(current_user.id)
    return balance

@wallet_router.post("/top-up")
async def topup_wallet(current_user: Annotated[User, Depends(get_current_active_user)],
    card_id: int,
    amount: float):

    wallet = add_money_to_wallet(current_user.id, card_id, amount)
    return wallet


@wallet_router.post("/withdraw")
async def withdraw_money(
    current_user: Annotated[User, Depends(get_current_active_user)],
    card_id: int,
    amount: float):

    wallet = withdraw_money_from_wallet(current_user.id, card_id, amount)
    return wallet