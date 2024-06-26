import uvicorn
from fastapi import FastAPI
from common.site_tweaks import description, tags_metadata
from routers.admin_router import admin_router
from routers.wallet_router import wallet_router
from routers.transaction_router import transaction_router
from routers.user_router import user_router
from routers.category_router import category_router
from routers.finance_router import finance_router
from routers.card_router import card_router
from routers.contact_router import contact_router

app = FastAPI(title="PayTheBills", description=description, openapi_tags=tags_metadata)


app.include_router(admin_router)
app.include_router(user_router)
app.include_router(transaction_router)
app.include_router(wallet_router)
app.include_router(category_router)
app.include_router(finance_router)
app.include_router(card_router)
app.include_router(contact_router)

if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=8001)
