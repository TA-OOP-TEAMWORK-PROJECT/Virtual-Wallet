from typing import Annotated, Dict
from fastapi import Depends, APIRouter, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


from common.auth import get_current_active_user, SECRET_KEY
from data_.models import User, UserTransfer, ExternalContacts, ConfirmationResponse, ExternalTransfer, Transactions, \
    RecurringTransaction
from services.transaction_service import user_transfer, get_transactions, sort_transactions, get_transaction_response, \
    change_status, bank_transfer, recurring_transactions, confirmation_respose, \
    get_recuring_transactions, process_to_user_approval, in_app_transfer, process_bank_transfer, \
    app_recurring_transaction, external_recurring_transaction, view_all_recuring_transactions
from services.user_service import find_by_username

transaction_router = APIRouter(prefix="/transactions", tags=["Transactions"])

scheduler = BackgroundScheduler()
external_pending_confirmations: Dict[str, Dict] = {}
internal_pending_confirmations: Dict[str, Dict] = {}




@transaction_router.on_event('startup')
async def startup_event():

    cron_trigger = CronTrigger(hour=12, minute=0)

    recurring_transactions()

    scheduler.start()


@transaction_router.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()


@transaction_router.get("/")
def view_transactions(current_user: Annotated[User, Depends(get_current_active_user)],
            sort:  str | None = None,
            sort_by: str | None = None,
            search: str | None = None):

    result = get_transactions(current_user, search)

    if sort_by and (sort == 'asc' or sort == 'desc'):
        result = sort_transactions(result, sort_by, is_reverse=sort == 'desc')

    return get_transaction_response(result)

@transaction_router.get("/recurring")
def view_recurring_transaction(current_user: Annotated[User, Depends(get_current_active_user)]):

    return view_all_recuring_transactions(current_user)


@transaction_router.post("/{username}")
def transfer_to_user(cur_transaction: UserTransfer, username: str,
                        current_user: Annotated[User, Depends(get_current_active_user)]):

    receiver = find_by_username(username)
    result = user_transfer(cur_transaction, receiver, current_user, True)
    return result


@transaction_router.post("/new_transaction/in_app")
def new_user_transaction(cur_transaction: UserTransfer,
                           search: str,
                           current_user: Annotated[User, Depends(get_current_active_user)]):

    transfer_message = in_app_transfer(cur_transaction, search, current_user)

    confirmation_id = "INTERNAL" + str(len(internal_pending_confirmations) + 1)
    internal_pending_confirmations[confirmation_id] = transfer_message

    return {"confirmation_id": confirmation_id, "message": "Please confirm the transaction:",
            "transaction": confirmation_respose(internal_pending_confirmations[confirmation_id], current_user.username)}


@transaction_router.post("/new_transaction/bank_transfer")
def create_bank_transfer(ext_user: ExternalContacts,
                         cur_transfer: UserTransfer,
                         current_user: Annotated[User, Depends(get_current_active_user)]):

    transfer_message = bank_transfer(ext_user, cur_transfer, current_user)

    confirmation_id = "EXTERNAL" + str(len(external_pending_confirmations) + 1)
    external_pending_confirmations[confirmation_id] = transfer_message

    return {"confirmation_id": confirmation_id, "message": "Please confirm the transaction:",
            "transaction": confirmation_respose(external_pending_confirmations[confirmation_id], ext_user.contact_name)}


@transaction_router.post("/transfer-confirmation/{confirmation_id}")
async def confirm_transfer(confirmation_id: str,
                           response: ConfirmationResponse):

    if confirmation_id not in external_pending_confirmations and confirmation_id not in internal_pending_confirmations:
        raise HTTPException(status_code=404, detail="Confirmation ID not found")

    if "INTERNAL" in confirmation_id:
        pending_request = internal_pending_confirmations[confirmation_id]
        process_to_user_approval(pending_request)
        del internal_pending_confirmations[confirmation_id]
        return "Transaction is processed and awaits approval from the user"

    else:
        pending_request = external_pending_confirmations[confirmation_id]
        if response.is_confirmed:

            process_bank_transfer(pending_request)
            del external_pending_confirmations[confirmation_id]
            return f"You have send the amount of {pending_request.transaction_amount}"

        else:
            del external_pending_confirmations[confirmation_id]
            return 'The transfer was denied!'


@transaction_router.post("/recurring/new-external")
def set_external_recurring_transaction(transaction: RecurringTransaction,
                              contact: ExternalContacts,
                            current_user: Annotated[User, Depends(get_current_active_user)]):

    result = external_recurring_transaction(transaction, contact, current_user)
    return result
    #get_transaction_by_id

@transaction_router.post("/recurring/new-in-app")
def set_app_recurring_transaction(transaction: RecurringTransaction,
                              contact: UserTransfer,
                              current_user: Annotated[User, Depends(get_current_active_user)]):

    result = app_recurring_transaction(transaction, contact, current_user)

    return result

#може да си сетнеш като погледнеш всички транзакции до сега които не са в приловението и да станат recurring

@transaction_router.put("/{transaction_id}/amount/status")  # да сложа search - Когато юзъра си стига само до транзакцията и сетва
def status_update(transaction_id: int, new_status: str,
                  current_user: Annotated[User, Depends(get_current_active_user)]):

    result = change_status(transaction_id, new_status, current_user)
    return result

# @transaction_router.put("/recurring_transactions/{transaction_id}/cancel")
# def create_recurring_transaction():
#     pass

