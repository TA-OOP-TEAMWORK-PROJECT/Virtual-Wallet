from typing import Annotated, Dict
from fastapi import Depends, APIRouter, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from jose import jwt

from common.auth import get_current_active_user, SECRET_KEY
from data_.models import User, UserTransfer, ExternalContacts, ConfirmationResponse, ExternalTransfer
from services.transaction_service import user_transfer, get_transactions, sort_transactions, get_transaction_response, \
    change_status, new_transfer, bank_transfer, recurring_transactions, process_transfer

transaction_router = APIRouter(prefix="/transactions", tags=["Transactions"])

scheduler = BackgroundScheduler()
pending_confirmations: Dict[str, Dict] = {}


@transaction_router.on_event('startup')
async def startup_event():

    cron_trigger = CronTrigger(hour=12, minute=0)

    recurring_transactions()

    scheduler.start() #




@transaction_router.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()




@transaction_router.post("/{username}")
def transfer_to_user(cur_transaction: UserTransfer, username: str,
                        current_user: Annotated[User, Depends(get_current_active_user)]):

    return user_transfer(cur_transaction, username, current_user)


@transaction_router.post("/new/in-app")
def create_new_transaction(cur_transaction: UserTransfer,
                           search: str,
                           current_user: Annotated[User, Depends(get_current_active_user)]):

    transfer_message = new_transfer(cur_transaction, search, current_user)

    confirmation_id = len(pending_confirmations)
    pending_confirmations[confirmation_id] = transfer_message

    return {"confirmation_id": confirmation_id, "message": "Please confirm the transaction"}



@transaction_router.post("/new/bank-transfer")
def create_bank_transfer(ext_user: ExternalTransfer,
                         cur_transaction: UserTransfer,
                         current_user: Annotated[User, Depends(get_current_active_user)]):

    transfer_message = bank_transfer(ext_user, cur_transaction, current_user)

    confirmation_id = len(pending_confirmations)
    pending_confirmations[confirmation_id] = transfer_message

    return {"confirmation_id": confirmation_id, "message": "Please confirm the transaction"}


@transaction_router.post("/confirm/{confirmation_id}")
async def confirm_transfer(confirmation_id: int,
                           response: ConfirmationResponse):


    if confirmation_id not in pending_confirmations:
        raise HTTPException(status_code=404, detail="Confirmation ID not found")


    pending_request = pending_confirmations[confirmation_id]

    # Check if the user confirmed the action
    if response.is_confirmed:
        # Process the money transfer (mock implementation)
        result = process_transfer(pending_request)   # изпращам заедно с информацията за трансфера за да бъде добавен към базата данни информацията е в модела при всички случай
        # Remove the confirmed request from the pending list
        del pending_confirmations[confirmation_id]
        return f"You have send the amount of {pending_request.transaction_amount}"

    else:
        # User did not confirm, do not proceed with the transfer
        del pending_confirmations[confirmation_id]
        return 'The transfer was denied!'

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


@transaction_router.post("/recurring/new")
def set_recurring_transaction(current_user: Annotated[User, Depends(get_current_active_user)]):
    #може да си сетнеш като погледнеш всички транзакции до сега които не са в приловението и да станат recurring

    result = create_recurring_transaction


@transaction_router.get("/recurring")
def create_recurring_transaction():
    pass

@transaction_router.put("/recurring/{transaction_id}/cancel")
def create_recurring_transaction():
    pass