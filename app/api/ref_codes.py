from fastapi import APIRouter, BackgroundTasks

from app.api.dependencies import DBDep, UserIdDep
from app.exceptions import (
    ReferalCodeAlreadyExistsException,
    ReferalCodeAlreadyExistsHTTPException,
    ReferalCodeNotFoundException,
    ReferalCodeNotFoundHTTPException,
    RemoveReferalCodeException,
    RemoveReferalCodeHTTPException,
)
from app.schemas.ref_codes import AddRequestRefCode
from app.services.auth import AuthService
from app.services.ref_codes import RefCodeService
from app.utils.utils import send_referral_email


refs_router = APIRouter(prefix="/ref_codes", tags=["Реферальные коды"])


@refs_router.get(
    "", summary="Получение информации о рефералах для текущего пользователя"
)
async def get_referral_users(db: DBDep, user_id: UserIdDep):
    return await RefCodeService(db).get_referral_users(user_id)


@refs_router.post("", summary="Создание реферального кода")
async def create_ref_code(
    db: DBDep,
    user_id: UserIdDep,
    background_tasks: BackgroundTasks,
    data: AddRequestRefCode,
):
    try:
        await RefCodeService(db).add_ref_code(data, user_id)
        user = await AuthService(db).get_me(user_id)
    except ReferalCodeNotFoundException:
        raise ReferalCodeNotFoundHTTPException
    except ReferalCodeAlreadyExistsException:
        raise ReferalCodeAlreadyExistsHTTPException
    except RemoveReferalCodeException:
        raise RemoveReferalCodeHTTPException

    background_tasks.add_task(
        send_referral_email, email_to=user.email, referral_code=data.code
    )

    return {"message": "Реферальный код успешно создан"}


@refs_router.delete("", summary="Удаление своего реферального кода")
async def delete_ref_code(db: DBDep, user_id: UserIdDep):
    try:
        await RefCodeService(db).remove_ref_code(user_id)
    except ReferalCodeNotFoundException:
        raise ReferalCodeNotFoundHTTPException

    return {"message": "Реферальный код успешно удален"}
