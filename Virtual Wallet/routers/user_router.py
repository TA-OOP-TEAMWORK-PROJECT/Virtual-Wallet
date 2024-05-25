from starlette import status
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from pydantic import constr
from fastapi.security import OAuth2PasswordRequestForm
from common.response import *
from data_.models import UserUpdate, AccountDetails, Token
from services import user_service
from common.auth import *
from services.user_service import get_user_response
from common.auth import (ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user,
                          create_access_token, get_current_active_user)

from common.auth import current_user

user_router = APIRouter(prefix='/users', tags=["Users"])


@user_router.get("/")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):

    return get_user_response(current_user)


@user_router.get("/details", response_model=AccountDetails)
async def get_account_details(current_user: Annotated[User, Depends(get_current_active_user)]):
    account_details = user_service.get_user_account_details(current_user.id)
    if not account_details:
        return NotFound(status_code=404, content="Account details not found")

    return account_details


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
        return {'message': f'User with username {user.username} has been created and awaits approval!'}
    else:
        return {'message': 'Failed to create user.'}, 500


@user_router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    user_credentials = current_user(form_data.username)

    user = authenticate_user(user_credentials, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@user_router.put("/update")
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