from typing import Annotated
from fastapi import Depends, APIRouter
from common.auth import get_current_active_user
from data_.models import User, UserTransfer, ExternalContacts
from services.transaction_service import user_transfer, get_transactions, sort_transactions, get_transaction_response, \
    change_status, new_transfer, bank_transfer

transaction_router = APIRouter(prefix="/transactions", tags=["Transactions"])
#pod transactions да се показва листа с приятели или тези на които си изпращал последно

@transaction_router.post("/{username}")
def transfer_to_user(cur_transaction: UserTransfer, username: str,
                        current_user: Annotated[User, Depends(get_current_active_user)]):

    return user_transfer(cur_transaction, username, current_user)



@transaction_router.post("/new_transaction/in_app")
def create_new_transaction(cur_transaction: UserTransfer,
                           search: str,
                           current_user: Annotated[User, Depends(get_current_active_user)],
                           ):

    return  new_transfer(cur_transaction, search, current_user)


@transaction_router.post("/new_transaction/bank_transfer")
def create_bank_transfer(ext_user: ExternalContacts,
                         cur_transaction: UserTransfer,
                         current_user: Annotated[User, Depends(get_current_active_user)]):

    return bank_transfer(ext_user, cur_transaction, current_user)


@transaction_router.get("/")
def view_transactions(current_user: Annotated[User, Depends(get_current_active_user)],
            sort:  str | None = None,
            sort_by: str | None = None,
            search: str | None = None):

    result = get_transactions(current_user, search)

    if sort and (sort == 'asc' or sort == 'desc'):
        result = sort_transactions(result, sort_by, is_reverse=sort == 'desc')

    return get_transaction_response(result)

@transaction_router.put("/{transaction_id}/amount/status")
def status_update(transaction_id: int, new_status: str,
                  current_user: Annotated[User, Depends(get_current_active_user)]):

    result = change_status(transaction_id, new_status)
    return result

