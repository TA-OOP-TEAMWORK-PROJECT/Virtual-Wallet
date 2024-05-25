# from datetime import timedelta
# from typing import Annotated
# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.security import OAuth2PasswordRequestForm
# from starlette import status
# from data_.models import Token, User
# from common.auth import (ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user,
#                           create_access_token, get_current_active_user)
#
# from common.auth import current_user
#
# auth_router = APIRouter(prefix='/auth', tags=["Auth"])
#
#
# @auth_router.post("/login", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#
#     user_credentials = current_user(form_data.username)
#
#     user = authenticate_user(user_credentials, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return Token(access_token=access_token, token_type="bearer")
#
#
#
