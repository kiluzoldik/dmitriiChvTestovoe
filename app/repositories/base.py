from pydantic import BaseModel
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.exceptions import ObjectAlreadyExistsException, ObjectNotFoundException


class BaseRepository:
    model = None
    mapper = None

    def __init__(self, session):
        self.session = session

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(add_stmt)
        except IntegrityError:
            raise ObjectAlreadyExistsException

        return result.scalar_one()

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        query = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning()
        )
        try:
            await self.session.execute(query)
        except NoResultFound:
            raise ObjectNotFoundException
