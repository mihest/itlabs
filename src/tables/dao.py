from typing import Optional, Union, Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, with_expression

from src.dao import BaseDAO
from src.tables.models import TableModel
from src.tables.schemas import UpdateTable


class TableDAO(BaseDAO[TableModel, None, UpdateTable]):
    model = TableModel

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
            .options(selectinload(cls.model.guests))
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
    ) -> Optional[TableModel]:
        stmt = select(cls.model).filter(*filters).filter_by(**filter_by).options(
            selectinload(cls.model.guests)
        )
        result = await session.execute(stmt)
        return result.scalars().one_or_none()


    @classmethod
    async def update(
            cls,
            session: AsyncSession,
            *where,
            obj_in: Union[UpdateTable, dict[str, Any]],
    ) -> Optional[TableModel]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True, exclude_none=True)

        stmt = update(cls.model).where(*where).values(**update_data).returning(cls.model)
        result = await session.execute(stmt)
        return result.scalars().one_or_none()
