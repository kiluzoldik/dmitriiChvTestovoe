from app.exceptions import (
    ReferalCodeAlreadyExistsException,
    ReferalCodeNotFoundException,
    RemoveReferalCodeException,
)
from app.repositories.redis.redis_manager import redis_manager
from app.repositories.ref_codes import RefCodesRepository
from app.schemas.ref_codes import AddRequestRefCode, RefCode
from app.services.base import BaseService


class RefCodeService(BaseService):
    async def get_referral_users(self, user_id: int):
        return await RefCodesRepository(self.db.session).get_referrals_by_user(user_id)

    async def add_ref_code(self, data: AddRequestRefCode, user_id: int):
        code = await RefCodesRepository(self.db.session).check_ref_code_by_id(user_id)
        if not code:
            new_data = RefCode(code=data.code, expire=data.expire, user_id=user_id)
            await RefCodesRepository(self.db.session).add_ref_code(new_data)
        else:
            redis_code = await redis_manager.check_code(code)
            if code and redis_code:
                raise ReferalCodeAlreadyExistsException
            else:
                raise RemoveReferalCodeException

        await self.db.commit()

    async def remove_ref_code(self, user_id: int):
        code = await RefCodesRepository(self.db.session).check_ref_code_by_id(user_id)
        if not code:
            raise ReferalCodeNotFoundException

        await RefCodesRepository(self.db.session).remove_ref_code(code, user_id)
        await self.db.commit()
