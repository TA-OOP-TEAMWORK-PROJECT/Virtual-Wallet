from fastapi import APIRouter, Depends, HTTPException
from services import user_service
from common.auth import *

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