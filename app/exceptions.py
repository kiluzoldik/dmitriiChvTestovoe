from fastapi import HTTPException


class BaseDmitriiChvException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class BaseDmitriiChvHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(detail=self.detail, status_code=self.status_code)


class ObjectNotFoundException(BaseDmitriiChvException):
    detail = "Объект не найден"


class UserNotFoundException(BaseDmitriiChvException):
    detail = "Пользователь не найден"


class UserNotFoundHTTPException(BaseDmitriiChvHTTPException):
    status_code = 404
    detail = "Пользователь не найден"


class UserEmailNotFoundException(BaseDmitriiChvException):
    detail = "Пользователь с таким email не найден"


class UserEmailNotFoundHTTPException(BaseDmitriiChvHTTPException):
    status_code = 404
    detail = "Пользователь с таким email не найден"


class EmailPasswordValidationException(BaseDmitriiChvException):
    detail = "Неверный email или пароль"


class EmailPasswordValidationHTTPException(BaseDmitriiChvHTTPException):
    status_code = 401
    detail = "Неверный email или пароль"


class ObjectAlreadyExistsException(BaseDmitriiChvException):
    detail = "Объект уже существует"


class UserEmailAlreadyExistsException(BaseDmitriiChvException):
    detail = "Пользователь с таким email уже существует"


class UserEmailAlreadyExistsHTTPException(BaseDmitriiChvHTTPException):
    status_code = 409
    detail = "Пользователь с таким email уже существует"


class FullNameLengthHTTPException(BaseDmitriiChvHTTPException):
    status_code = 400
    detail = "ФИО должно содержать не менее 10 символов"


class FullNameValidationHTTPException(BaseDmitriiChvHTTPException):
    status_code = 400
    detail = "ФИО не должно содержать чисел"


class LengthPasswordHTTPException(BaseDmitriiChvHTTPException):
    status_code = 400
    detail = "Пароль должен быть не менее 8 символов"


class DigitPasswordHTTPException(BaseDmitriiChvHTTPException):
    status_code = 400
    detail = "Пароль должен содержать хотя бы одну цифру"


class UpperLetterPasswordHTTPException(BaseDmitriiChvHTTPException):
    status_code = 400
    detail = "Пароль должен содержать хотя бы одну заглавную букву"


class SpecialSimbolPasswordHTTPException(BaseDmitriiChvHTTPException):
    status_code = 400
    detail = "Пароль должен содержать хотя бы один спецсимвол"


class EmailException(BaseDmitriiChvException):
    detail = "Неверный формат Email"


class EmailHTTPException(BaseDmitriiChvHTTPException):
    status_code = 400
    detail = "Неверный формат Email"


class ReferalCodeException(BaseDmitriiChvException):
    detail = "Неверный реферальный код"


class ReferalCodeHTTPException(BaseDmitriiChvHTTPException):
    status_code = 400
    detail = "Неверный реферальный код"


class ReferalCodeAlreadyExistsException(BaseDmitriiChvException):
    detail = "У вас уже есть реферальный код"


class ReferalCodeAlreadyExistsHTTPException(BaseDmitriiChvHTTPException):
    status_code = 409
    detail = "У вас уже есть реферальный код"


class ReferalCodeNotFoundException(BaseDmitriiChvException):
    detail = "Реферальный код не найден"


class ReferalCodeNotFoundHTTPException(BaseDmitriiChvHTTPException):
    status_code = 404
    detail = "Реферальный код не найден"


class EmailSenderException(BaseDmitriiChvException):
    detail = "Неожиданная ошибка при отправке сообщения на email"


class RemoveReferalCodeException(BaseDmitriiChvException):
    detail = "Срок старого реферального кода истёк, пожалуйста, удалите существующий код и создайте новый"


class RemoveReferalCodeHTTPException(BaseDmitriiChvHTTPException):
    status_code = 400
    detail = "Срок старого реферального кода истёк, пожалуйста, удалите существующий код и создайте новый"
