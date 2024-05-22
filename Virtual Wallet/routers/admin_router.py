from data_.models import User
from fastapi import APIRouter, Depends, HTTPException
from services.admin_service import block_user, unblock_user
from common.auth import get_current_admin_user
from common.response import BadRequest, NotFound, Unauthorized, MessageServiceError

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