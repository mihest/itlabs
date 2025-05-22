import uuid

from fastapi import APIRouter, Depends

from src.database import SessionDep
from src.guests.schemas import GuestFilter, GuestResponse, UpdateGuest
from src.guests.service import GuestService

router = APIRouter()


@router.get("",
            name="Retrieves the collection of GuestList resources.",
            description="Retrieves the collection of GuestList resources.",)
async def get_list_guests(
        session: SessionDep,
        filters: GuestFilter = Depends()
) -> list[GuestResponse]:
    return await GuestService.get_list(session, filters)


@router.get("/{guest_id}",
            name="Retrieves a Guest by ID.",
            description="Retrieves a Guest by ID.",)
async def get_guest(
        guest_id: uuid.UUID,
        session: SessionDep,
) -> GuestResponse:
    return await GuestService.get_by_id(session, guest_id)

@router.patch("/{guest_id}",
             name="Updates a Guest resource.",
              description="Updates a Guest resource.",)
async def update_guest(
        guest_id: uuid.UUID,
        data: UpdateGuest,
        session: SessionDep,
) -> GuestResponse:
    return await GuestService.update(session, guest_id, data)