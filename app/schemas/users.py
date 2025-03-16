from pydantic import BaseModel, field_validator

from app.exceptions import (
    DigitPasswordHTTPException,
    FullNameLengthHTTPException,
    FullNameValidationHTTPException,
    LengthPasswordHTTPException,
    SpecialSimbolPasswordHTTPException,
    UpperLetterPasswordHTTPException,
)


class AddRequestUser(BaseModel):
    full_name: str
    email: str
    password: str
    other_referal_code: str | None = None

    @field_validator("full_name")
    @classmethod
    def validate_name(cls, value: str):
        if len(value) < 10:
            raise FullNameLengthHTTPException
        if any(v.isdigit() for v in value):
            raise FullNameValidationHTTPException
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise LengthPasswordHTTPException
        if not any(c.isdigit() for c in value):
            raise DigitPasswordHTTPException
        if not any(c.isupper() for c in value):
            raise UpperLetterPasswordHTTPException
        if not any(c in "!@#$%^&*()-_=+[]{};:,.<>?/|" for c in value):
            raise SpecialSimbolPasswordHTTPException
        return value


class LoginUserRequest(BaseModel):
    email: str
    password: str


class AddUser(BaseModel):
    full_name: str
    email: str
    hashed_password: str
    other_referal_code: str | None = None


class User(BaseModel):
    id: int
    full_name: str
    email: str
    user_referal_code: str | None = None
    other_referal_code: str | None = None


class ReferralUsers(BaseModel):
    id: int
    full_name: str
    other_referal_code: str | None = None


class UserWithHashedPassword(User):
    hashed_password: str
