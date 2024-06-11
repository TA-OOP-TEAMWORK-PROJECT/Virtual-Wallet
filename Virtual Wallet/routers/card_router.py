from typing import Annotated
from fastapi import APIRouter, Depends
from common.auth import get_current_active_user
from data_.models import Card, User
from services.card_service import delete, add, shop_online

card_router = APIRouter(prefix='/cards', tags=["Cards"])


@card_router.post("/add")
async def add_new(card: Card,
                  current_user: Annotated[User, Depends(get_current_active_user)]):

    command = 'add'
    return add(card, current_user.id, command)


@card_router.post("/create")
async def create_new_card(card: Card,
                          current_user: Annotated[User, Depends(get_current_active_user)]):

    command = 'create'
    return add(card, current_user.id, command)


@card_router.post("/virtual/online-purchases") #Easter egg
async def online_purchase(current_user: Annotated[User, Depends(get_current_active_user)], card_id: int, amount: float):
    return shop_online(current_user.id, card_id, amount)


@card_router.put("/delete/{card_id}")
async def delete_card(card_id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    return delete(card_id, current_user.id)