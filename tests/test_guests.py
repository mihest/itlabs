import uuid

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.guests.models import GuestModel
from src.tables.models import TableModel
from tests.conftest import async_session_maker


async def get_first():
    async with async_session_maker() as session:
        stmt = (
            select(GuestModel)
            .options(selectinload(GuestModel.table).selectinload(TableModel.guests))
        )
        result = await session.execute(stmt)
        return result.scalars().first()


async def test_get_list(ac: AsyncClient):
    response = await ac.get("/api/guest_lists")
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data[0]["name"], str)
    assert isinstance(data[0]["isPresent"], bool)
    assert isinstance(data[0]["table"], dict)

    assert isinstance(data[0]["table"]["num"], int)
    assert data[0]["table"]["num"] > 0

    assert isinstance(data[0]["table"]["maxGuests"], int)
    assert data[0]["table"]["maxGuests"] > 0

    assert isinstance(data[0]["table"]["guestsDef"], int)
    assert data[0]["table"]["guestsDef"] >= 0

    assert isinstance(data[0]["table"]["guestsNow"], int)
    assert data[0]["table"]["guestsNow"] >= 0

    assert isinstance(data[0]["table"]["description"], str)


async def test_get_by_id(ac: AsyncClient):
    guest = await get_first()

    response = await ac.get(f"/api/guest_lists/{guest.id}")
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(guest.id)
    assert data["name"] == guest.name
    assert data["isPresent"] == guest.is_present

    assert data["table"]["id"] == str(guest.table.id)
    assert data["table"]["num"] == guest.table.num
    assert data["table"]["description"] == guest.table.description
    assert data["table"]["maxGuests"] == guest.table.max_guests
    assert data["table"]["guestsDef"] == guest.table.guests_count
    assert data["table"]["guestsNow"] == guest.table.guests_present_count


async def test_update(ac: AsyncClient):
    guest = await get_first()

    update_data = {
        "name": "asd",
        "isPresent": guest.is_present == False,
    }
    response = await ac.patch(f"/api/guest_lists/{guest.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()

    assert data["name"] == update_data["name"]
    assert data["isPresent"] == update_data["isPresent"]


async def test_get_by_id_not_found(ac: AsyncClient):
    response = await ac.get(f"/api/guest_lists/{uuid.uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Guest not found"


async def test_update_not_found(ac: AsyncClient):
    response = await ac.patch(f"/api/guest_lists/{uuid.uuid4()}", json={
        "name": "asd",
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Guest not found"


async def test_update_table_not_found(ac: AsyncClient):
    guest = await get_first()
    response = await ac.patch(f"/api/guest_lists/{guest.id}", json={
        "tableId": str(uuid.uuid4()),
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Table not found"


