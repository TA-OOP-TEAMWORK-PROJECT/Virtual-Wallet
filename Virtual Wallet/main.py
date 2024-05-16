import uvicorn
from fastapi import FastAPI
from routers.auth_router import auth_router
from routers.admin_router import admin_router
from routers.transaction_router import transaction_router
from routers.user_router import user_router
from common.site_tweaks import *

app = FastAPI(title="PayTheBills",
    description=description, openapi_tags=tags_metadata)


app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(transaction_router)





if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=8001)