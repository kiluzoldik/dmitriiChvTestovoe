from fastapi import APIRouter, Response

from app.api.dependencies import DBDep, UserIdDep
from app.exceptions import (
    EmailException,
    EmailHTTPException,
    EmailPasswordValidationException,
    EmailPasswordValidationHTTPException,
    ReferalCodeException,
    ReferalCodeHTTPException,
    UserEmailNotFoundException,
    UserEmailNotFoundHTTPException,
    UserNotFoundException,
    UserNotFoundHTTPException,
)
from app.schemas.users import AddRequestUser, LoginUserRequest
from app.services.auth import AuthService


auth_router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@auth_router.get(
    "/me",
    summary="Информация о пользователе",
    description="<h1>Получение данных активного пользователя</h1>",
)
async def get_user_info(db: DBDep, user_id: UserIdDep):
    try:
        user_data = await AuthService(db).get_me(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException

    return {"message": "Информация о текущем пользователе", "detail": user_data}


@auth_router.post("/register", summary="Регистрация пользователя")
async def register_user(db: DBDep, data: AddRequestUser):
    try:
        await AuthService(db).register(data)
    except EmailException:
        raise EmailHTTPException
    except ReferalCodeException:
        raise ReferalCodeHTTPException

    return {"message": "Пользователь успешно зарегистрирован"}


@auth_router.post("/login", summary="Аутентификация пользователя")
async def login_user(db: DBDep, data: LoginUserRequest, response: Response):
    try:
        access_token = await AuthService(db).login(data, response)
    except UserEmailNotFoundException:
        raise UserEmailNotFoundHTTPException
    except EmailPasswordValidationException:
        raise EmailPasswordValidationHTTPException

    return {"access_token": access_token}


@auth_router.get("/logout", summary="Выход из аккаунта")
async def logout_user(db: DBDep, response: Response):
    await AuthService(db).logout(response)
    return {"message": "Вы успешно вышли из системы"}
