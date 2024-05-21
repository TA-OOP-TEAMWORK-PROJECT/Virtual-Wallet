from fastapi import APIRouter, Depends, HTTPException, Body, Query
from pydantic import constr

from common.response import *
from data_.models import UserUpdate, AccountDetails, ExternalContacts
from services import user_service
from common.auth import *
from services.user_service import get_user_response

user_router = APIRouter(prefix='/users', tags=["Users"])


@user_router.post('/register')
def register(user_data: User):
    user = user_service.create(
        user_data.username,
        user_data.password,
        user_data.first_name,
        user_data.last_name,
        user_data.email,
        user_data.phone_number
    )
    if user is not None:
        return {'message': f'User with username {user.username} has been created!'}
    else:
        return {'message': 'Failed to create user.'}, 500


@user_router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):

    return get_user_response(current_user)


@user_router.put("/me")
async def update_user_profile(
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_update: UserUpdate = Body(...)
):
    if not user_update.email:
        user_update.email = current_user.email
    if not user_update.phone_number:
        user_update.phone_number = current_user.phone_number
    if not user_update.password:
        user_update.password = None

    update_message = user_service.update_user_profile(current_user.username, user_update)
    if update_message is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update user profile."
        )
    return {"message": update_message}


@user_router.get("/me/details", response_model=AccountDetails)
async def get_account_details(current_user: Annotated[User, Depends(get_current_active_user)]):
    account_details = user_service.get_user_account_details(current_user.id)
    if not account_details:
        return NotFound(status_code=404, content="Account details not found")

    return account_details


@user_router.get("/contacts") #Could
async def view_contacts_list(current_user: Annotated[User, Depends(get_current_active_user)]):
    contacts = user_service.view_user_contacts(current_user.id)
    return contacts


@user_router.post("/contacts") #Could
async def add_contact(current_user: Annotated[User, Depends(get_current_active_user)], contact_request: constr(min_length=2, max_length=20)):
    contact = user_service.add_user_to_contacts(current_user.id, contact_request)
    return contact


@user_router.post("/contacts/external")
async def add_external_contact(
    current_user: Annotated[User, Depends(get_current_active_user)],
    contact_data: ExternalContacts
):
    contact = user_service.add_external_contact(current_user.id, contact_data)
    return contact


@user_router.get("/contacts/search")
async def search_contacts(
    current_user: Annotated[User, Depends(get_current_active_user)],
    search: str,
    contact_list: bool = Query(False)
):
    contacts = user_service.get_username_by(current_user.id, search, contact_list)
    return contacts