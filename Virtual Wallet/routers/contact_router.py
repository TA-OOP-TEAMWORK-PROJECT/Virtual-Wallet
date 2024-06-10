from fastapi import APIRouter, Depends, HTTPException, Body, Query
from pydantic import constr, Field
import asyncio
from common.response import *
from data_.models import UserUpdate, AccountDetails, ExternalContacts
from services import contact_service
from common.auth import *
from services.contact_service import view_user_contacts, add_user_to_contacts, get_username_by, \
    remove_from_contacts, add_external_user_to_contacts

contact_router = APIRouter(prefix='/contacts', tags=["Contacts"])


@contact_router.get("/") #Could
async def view_contacts_list(current_user: Annotated[User, Depends(get_current_active_user)]):
    contacts = view_user_contacts(current_user.id)
    return contacts


@contact_router.get("/search")
async def search_contacts(
    current_user: Annotated[User, Depends(get_current_active_user)],
    search: str,
    contact_list: bool = Query(False)
):
    contacts = get_username_by(current_user.id, search, contact_list)
    return contacts



@contact_router.post("/add") #Could
async def add_contact(current_user: Annotated[User, Depends(get_current_active_user)], contact_request: constr(min_length=2, max_length=20)):
    contact = add_user_to_contacts(current_user.id, contact_request)
    return contact


@contact_router.post("/add/external")
async def add_external_contact(
    current_user: Annotated[User, Depends(get_current_active_user)],
    contact_data: ExternalContacts
):
    contact = add_external_user_to_contacts(current_user.id, contact_data)
    return contact


@contact_router.delete("/remove")
async def remove_contact(
    current_user: Annotated[User, Depends(get_current_active_user)],
    removed_user_id: int
):
    success = remove_from_contacts(current_user.id, removed_user_id)
    if success:
        return "Contact removed successfully."
    else:
        raise HTTPException(status_code=500, detail="Failed to remove contact.")