from fastapi import APIRouter, Depends, HTTPException
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



