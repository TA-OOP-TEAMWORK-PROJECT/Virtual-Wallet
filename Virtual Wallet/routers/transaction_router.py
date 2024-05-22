from typing import Annotated
from fastapi import Depends, APIRouter
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from jose import jwt

from common.auth import get_current_active_user, SECRET_KEY
from data_.models import User, UserTransfer, ExternalContacts
from services.transaction_service import user_transfer, get_transactions, sort_transactions, get_transaction_response, \
    change_status, new_transfer, bank_transfer, recurring_transactions

transaction_router = APIRouter(prefix="/transactions", tags=["Transactions"])

scheduler = BackgroundScheduler()



"""new_day = calculate_new_day()
        new_hour = calculate_new_hour()
        new_minute = calculate_new_minute()

        # Update the CronTrigger with the new parameters
        cron_trigger.day = new_day
        cron_trigger.hour = new_hour
        cron_trigger.minute = new_minute"""



@transaction_router.on_event('startup')
async def startup_event():

    cron_trigger = CronTrigger(hour=12, minute=0)

    recurring_transactions()

    scheduler.start() #




# @transaction_router.on_event("shutdown")
# def shutdown_event():
#     scheduler.shutdown()
#



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

