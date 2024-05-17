from typing import Annotated
from fastapi import APIRouter, Depends

from common.auth import get_current_active_user
from data_.models import Card, User
from services import card_service

card_router = APIRouter(prefix='/cards', tags=["Cards"])


@card_router.post("/add")
async def add_new(cur_card: Card,
                  current_user: Annotated[User, Depends(get_current_active_user)]):

    return card_service.add(cur_card, current_user.id)


