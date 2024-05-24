from typing import Annotated
from fastapi import APIRouter, Depends

from common.auth import get_current_active_user
from data_.models import Card, User
from services import wallet_service
from services.wallet_service import delete, add_money_to_wallet, withdraw_money_from_wallet, get_wallet_balance

wallet_router = APIRouter(prefix='/wallets', tags=["Wallet"])


@wallet_router.post("/add/card")
async def add_new(card: Card,
                  current_user: Annotated[User, Depends(get_current_active_user)]):

    command = 'add'
    return wallet_service.add(card, current_user.id, command)


@wallet_router.post("/create/card")
async def create_new_card(card: Card,
                          current_user: Annotated[User, Depends(get_current_active_user)]):

    command = 'create'
    return wallet_service.add(card, current_user.id, command)


@wallet_router.put("/delete/{card_id}")
async def delete_card(card_id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    return delete(card_id, current_user.id)


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


@wallet_router.get("/balance")
async def get_balance(
    current_user: Annotated[User, Depends(get_current_active_user)]):
    balance = get_wallet_balance(current_user.id)
    return balance