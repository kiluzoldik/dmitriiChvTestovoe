from typing import Annotated

from fastapi import Depends, HTTPException, Request
from app.services.auth import AuthService
from app.utils.db_manager import DBManager
from app.database import async_session_maker


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(
            status_code=401, detail="Токен отсутствует или недействителен"
        )
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    try:
        data = AuthService().decode_token(token)
    except Exception:
        raise HTTPException(
            status_code=401, detail="Ошибка аутентификации: токен недействителен"
        )
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]
