from datetime import date, datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from data_.models import Transactions, User
from services.admin_service import deny_pending_transaction, get_all_transactions, get_pending_transactions, get_all_users

admin_router = APIRouter(prefix='/admins')

from services.admin_service import block_user, unblock_user, get_user
from common.auth import get_current_admin_user
from common.response import BadRequest, NotFound, Unauthorized, MessageServiceError
from services.admin_service import approve_user

admin_router = APIRouter(prefix='/admin', tags=["Admin"])

@admin_router.put("/block_user/{user_id}")
async def block_user_endpoint(user_id: int, admin: User = Depends(get_current_admin_user)):
    if not admin:
        return HTTPException(status_code=401, content='You are not authorized!')
    try:
        block_user(user_id)
        return {'message": "User blocked successfully'}
    except MessageServiceError as e:
        raise NotFound(content=str(e))


@admin_router.put("/unblock_user/{user_id}")
async def unblock_user_endpoint(user_id: int, admin: User = Depends(get_current_admin_user)):
    if not admin:
        raise HTTPException(status_code=401, detail="You are not authorized!")
    try:
        unblock_user(user_id)
        return {'message": "User unblocked successfully'}
    except MessageServiceError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@admin_router.post('/approve/{user_id}')
def approve_registration(user_id: int, admin: User = Depends(get_current_admin_user)):
    if not admin:
        raise HTTPException(status_code=401, detail='You are not authorized!')
    try:
        approve_user(user_id)
        return {'message': 'User approved successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@admin_router.get('/get_all_transactions')
def get_all_transactions_route(admin: User = Depends(get_current_admin_user),
                               page: int = 1,
                               page_size: int = 10,
                               period_start: Optional[date] = None,
                               period_end: Optional[date] = None,
                               sender_id: Optional[int] = None,
                               receiver_id: Optional[int] = None,
                               direction: Optional[str] = None,
                               sort_by: Optional[str] = None) -> List[Transactions]:
    if not admin:
        raise HTTPException(status_code=401, detail='You are not authorized!')
    try:
        transactions = get_all_transactions(page, page_size, period_start, period_end, sender_id, receiver_id, direction, sort_by)
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@admin_router.get('/get_pending_transactions')
def get_pending_transactions_route(admin: User = Depends(get_current_admin_user)):
    if not admin:
        raise HTTPException(status_code=401, detail='You are not authorized!')
    try:
        transactions = get_pending_transactions()
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@admin_router.get('/get_all_users')
def get_all_users_route(page: int = 1, admin: User = Depends(get_current_admin_user)):
    if not admin:
        raise HTTPException(status_code=401, detail='You are not authorized!')
    try:
        users = get_all_users(page)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@admin_router.get("/users/{search_type}/{search_value}", response_model=list[User])
async def get_user_by_search_type(search_type: str, search_value: str, admin: User = Depends(get_current_admin_user)):
    if not admin:
        raise HTTPException(status_code=401, detail='You are not authorized!')
    if search_type not in ["id", "username", "email", "phone"]:
        raise HTTPException(status_code=400, detail="Invalid search type. Must be one of 'id', 'username', 'email', or 'phone'.")
    
    users = get_user(search_type, search_value)
    
    if not users:
        raise HTTPException(status_code=404, detail="User not found.")
    
    for user in users:
        user.password = None
        user.hashed_password = None
        
    return users

@admin_router.post('/deny_pending_transaction/{transaction_id}')
def cancel_transaction_route(transaction_id: int, admin: User = Depends(get_current_admin_user)):
    if not admin:
        raise HTTPException(status_code=401, detail='You are not authorized!')
    try:
        deny_pending_transaction(transaction_id)
        return {"detail": "Transaction denied successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))