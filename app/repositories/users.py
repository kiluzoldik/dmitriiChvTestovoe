from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.exceptions import UserEmailNotFoundException
from app.repositories.base import BaseRepository
from app.models.users import UsersORM
from app.repositories.mappers.mappers import (
    UserDataMapper,
    UserWithHashedPasswordDataMapper,
)


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: str):
        stmt = select(self.model).filter_by(email=email)
        try:
            result = await self.session.execute(stmt)
            model = result.scalar_one()
        except NoResultFound:
            raise UserEmailNotFoundException
        return UserWithHashedPasswordDataMapper.map_to_domain_entity(model)
