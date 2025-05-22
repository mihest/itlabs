from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.dao import BaseDAO
from src.guests.models import GuestModel
from src.guests.schemas import UpdateGuest
from src.tables.models import TableModel


class GuestDAO(BaseDAO[GuestModel, None, UpdateGuest]):
    model = GuestModel

    @classmethod
    async def find_all(
            cls,
            session: AsyncSession,
            *filters,
            offset: int = 0,
            limit: int = 100,
            order_by: str = None,
            **filter_by,
    ):
        stmt = (
            select(cls.model)
            .options(
                selectinload(cls.model.table).options(selectinload(TableModel.guests))
            )
            .filter(*filters)
            .filter_by(**filter_by)
            .offset(offset)
            .limit(limit)
            .order_by(order_by)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def find_one_or_none(
            cls,
            session: AsyncSession,
            *filters,
            **filter_by
    ) -> Optional[GuestModel]:
        stmt = (
            select(cls.model)
            .options(selectinload(cls.model.table).selectinload(TableModel.guests))
            .filter(*filters)
            .filter_by(**filter_by)
        )
        result = await session.execute(stmt)
        return result.scalars().one_or_none()