import uuid

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.tables.dao import TableDAO
from src.tables.models import TableModel
from src.tables.schemas import TableFilter, TableResponse, TableGuestResponse, TableStatsResponse, UpdateTable


class TableService:
    @classmethod
    async def get_list(cls, session: AsyncSession, filters: TableFilter):
        filt = []
        if filters.nums:
            filt.append(TableModel.num.in_(filters.nums))

        tables = await TableDAO.find_all(session, *filt, order_by="num")
        return [
            TableResponse(
                id=table.id,
                num=table.num,
                description=table.description,
                maxGuests=table.max_guests,
                guestsDef=table.guests_count,
                guestsNow=table.guests_present_count,
                guests=[
                    TableGuestResponse(
                        id=guest.id,
                        name=guest.name,
                        isPresent=guest.is_present
                    ) for guest in table.guests
                ]
            ) for table in tables
        ]

    @classmethod
    async def get_by_id(cls, session: AsyncSession, table_id: uuid.UUID):
        table = await TableDAO.find_one_or_none(session, TableModel.id == table_id)
        if not table:
            raise HTTPException(status_code=404, detail="Table not found")
        return TableResponse(
                id=table.id,
                num=table.num,
                description=table.description,
                maxGuests=table.max_guests,
                guestsDef=table.guests_count,
                guestsNow=table.guests_present_count,
                guests=[
                    TableGuestResponse(
                        id=guest.id,
                        name=guest.name,
                        isPresent=guest.is_present
                    ) for guest in table.guests
                ]
            )

    @classmethod
    async def get_guests_by_id(cls, session: AsyncSession, table_id: uuid.UUID):
        table = await TableDAO.find_one_or_none(session, TableModel.id == table_id)
        if not table:
            raise HTTPException(status_code=404, detail="Table not found")

        return [
            TableGuestResponse(
                id=guest.id,
                name=guest.name,
                isPresent=guest.is_present
            ) for guest in table.guests
        ]

    @classmethod
    async def get_stats(cls, session: AsyncSession, filters: TableFilter):
        filt = []
        if filters.nums:
            filt.append(TableModel.num.in_(filters.nums))

        tables = await TableDAO.find_all(session, *filt, order_by="num")
        return [
            TableStatsResponse(
                id=table.id,
                num=table.num,
                maxGuests=table.max_guests,
                booking=table.guests_count,
                guestIsPresent=table.guests_present_count
            ) for table in tables
        ]

    @classmethod
    async def update(cls, session: AsyncSession, table_id: uuid.UUID, data: UpdateTable):
        if not data.model_dump(exclude_unset=True):
            raise HTTPException(status_code=400, detail="Body cannot be empty")

        table = await TableDAO.find_one_or_none(session, TableModel.id == table_id)
        if not table:
            raise HTTPException(status_code=404, detail="Table not found")

        try:
            updated_table = await TableDAO.update(session, TableModel.id == table_id, obj_in=data)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Table num already exists")

        return TableResponse(
            id=updated_table.id,
            num=updated_table.num,
            description=updated_table.description,
            maxGuests=updated_table.max_guests,
            guestsDef=updated_table.guests_count,
            guestsNow=updated_table.guests_present_count,
            guests=[
                TableGuestResponse(
                    id=guest.id,
                    name=guest.name,
                    isPresent=guest.is_present
                ) for guest in updated_table.guests
            ]
        )

