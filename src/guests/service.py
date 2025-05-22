import uuid

from fastapi import HTTPException

from src.guests.dao import GuestDAO
from src.guests.models import GuestModel
from src.guests.schemas import GuestFilter, GuestResponse, GuestTableResponse, UpdateGuest
from src.tables.dao import TableDAO
from src.tables.models import TableModel


class GuestService:
    @classmethod
    async def get_list(cls, session, filters: GuestFilter):
        filt = []
        if filters.is_present is not None:
            filt.append(GuestModel.is_present == filters.is_present)
        if filters.name:
            filt.append(GuestModel.name.ilike(f"%{filters.name}%"))

        guests = await GuestDAO.find_all(session, *filt)
        return [GuestResponse(
            id=guest.id,
            name=guest.name,
            isPresent=guest.is_present,
            table=GuestTableResponse(
                id=guest.table.id,
                num=guest.table.num,
                description=guest.table.description,
                maxGuests=guest.table.max_guests,
                guestsDef=guest.table.guests_count,
                guestsNow=guest.table.guests_present_count
            )
        ) for guest in guests]

    @classmethod
    async def get_by_id(cls, session, guest_id: uuid.UUID):
        guest = await GuestDAO.find_one_or_none(session, GuestModel.id == guest_id)
        if guest is None:
            raise HTTPException(status_code=404, detail="Guest not found")

        return GuestResponse(
            id=guest.id,
            name=guest.name,
            isPresent=guest.is_present,
            table=GuestTableResponse(
                id=guest.table.id,
                num=guest.table.num,
                description=guest.table.description,
                maxGuests=guest.table.max_guests,
                guestsDef=guest.table.guests_count,
                guestsNow=guest.table.guests_present_count
            )
        )

    @classmethod
    async def update(cls, session, guest_id: uuid.UUID, data: UpdateGuest):
        if not data.model_dump(exclude_unset=True):
            raise HTTPException(status_code=400, detail="Body cannot be empty")

        guest = await GuestDAO.find_one_or_none(session, GuestModel.id == guest_id)
        if not guest:
            raise HTTPException(status_code=404, detail="Guest not found")
        if data.table_id:
            table = await TableDAO.find_one_or_none(session, TableModel.id == data.table_id)
            if not table:
                raise HTTPException(status_code=404, detail="Table not found")

        updated_guest = await GuestDAO.update(session, GuestModel.id == guest_id, obj_in=data)
        return GuestResponse(
            id=updated_guest.id,
            name=updated_guest.name,
            isPresent=updated_guest.is_present,
            table=GuestTableResponse(
                id=updated_guest.table.id,
                num=updated_guest.table.num,
                description=updated_guest.table.description,
                maxGuests=updated_guest.table.max_guests,
                guestsDef=updated_guest.table.guests_count,
                guestsNow=updated_guest.table.guests_present_count
            )
        )