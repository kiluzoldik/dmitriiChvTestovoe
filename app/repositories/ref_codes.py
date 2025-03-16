from pydantic import BaseModel
from sqlalchemy import select, update

from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import ReferralUsersDataMapper
from app.schemas.ref_codes import RefCode
from app.repositories.redis.redis_manager import redis_manager
from app.models.users import UsersORM


class RefCodesRepository(BaseRepository):
    mapper = ReferralUsersDataMapper

    async def get_referrals_by_user(self, user_id: int) -> list[BaseModel]:
        code = await self.check_ref_code_by_id(user_id)
        query = select(UsersORM).where(UsersORM.other_referal_code == code)
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(data)
            for data in result.scalars().all()
            if data.other_referal_code is not None
        ]

    async def add_ref_code(self, data: RefCode):
        await redis_manager.save_data(data)
        query = (
            update(UsersORM)
            .where(UsersORM.id == data.user_id)
            .values(user_referal_code=data.code)
        )
        await self.session.execute(query)

    async def remove_ref_code(self, code: str, user_id: int):
        await redis_manager.remove_code(code)
        query = (
            update(UsersORM)
            .where(UsersORM.id == user_id)
            .values(user_referal_code=None)
        )
        await self.session.execute(query)

    async def check_ref_code_by_id(self, user_id: int):
        query = (
            select(UsersORM.user_referal_code)
            .select_from(UsersORM)
            .where(UsersORM.id == user_id)
        )
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
