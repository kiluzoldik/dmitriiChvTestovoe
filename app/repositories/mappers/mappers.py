from app.models.users import UsersORM
from app.repositories.mappers.base import DataMapper
from app.schemas.users import ReferralUsers, User, UserWithHashedPassword


class UserDataMapper(DataMapper):
    model = UsersORM
    schema = User


class UserWithHashedPasswordDataMapper(DataMapper):
    model = UsersORM
    schema = UserWithHashedPassword


class ReferralUsersDataMapper(DataMapper):
    model = UsersORM
    schema = ReferralUsers
