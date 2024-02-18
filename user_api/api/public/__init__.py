from fastapi import APIRouter, Depends

from api.auth import authent
from api.public.user import views as users
from api.public.health import views as health
from api.public.chat import views as chat

api = APIRouter()


api.include_router(
    health.router,
    prefix="/health",
    tags=["Health"],
    dependencies=[Depends(authent)],
)
api.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(authent)],
)
api.include_router(
    chat.router,
    prefix="/chat",
    tags=["Chat"],
    dependencies=[Depends(authent)],
)

