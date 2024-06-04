from fastapi import APIRouter, Depends
from common.auth import get_current_active_user
from data_.models import User, Categories
from services import category_service
from typing import Annotated

category_router = APIRouter(prefix='/categories', tags=["Categories"])


@category_router.get("/")
async def view_categories(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return category_service.view_categories(current_user.id)


@category_router.post("/")
async def create_category(
    title: str,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return category_service.create_category(current_user.id, title)


@category_router.post("/{category_id}/transactions/{transaction_id}")
async def link_transaction(current_user: Annotated[User, Depends(get_current_active_user)],
    transaction_id: int,
    category_id: int,
):
    return category_service.link_transaction_to_category(current_user.id, transaction_id, category_id)