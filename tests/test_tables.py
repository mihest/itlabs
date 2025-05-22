import uuid

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.tables.models import TableModel
from tests.conftest import async_session_maker


async def get_first():
    async with async_session_maker() as session:
        stmt = (
            select(TableModel)
            .options(selectinload(TableModel.guests))
        )
        result = await session.execute(stmt)
        return result.scalars().first()


async def test_get_list(ac: AsyncClient):
    response = await ac.get("/api/tables")
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data[0]["num"], int)
    assert data[0]["num"] > 0

    assert isinstance(data[0]["maxGuests"], int)
    assert data[0]["maxGuests"] > 0

    assert isinstance(data[0]["guestsDef"], int)
    assert data[0]["guestsDef"] >= 0

    assert isinstance(data[0]["guestsNow"], int)
    assert data[0]["guestsNow"] >= 0

    assert isinstance(data[0]["description"], str)

    assert isinstance(data[0]["guests"][0], dict)
    assert isinstance(data[0]["guests"][0]["name"], str)
    assert isinstance(data[0]["guests"][0]["isPresent"], bool)


async def test_get_stats(ac: AsyncClient):
    response = await ac.get("/api/tables_stats")
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data[0]["num"], int)
    assert data[0]["num"] > 0

    assert isinstance(data[0]["maxGuests"], int)
    assert data[0]["maxGuests"] > 0

    assert isinstance(data[0]["booking"], int)
    assert data[0]["booking"] >= 0

    assert isinstance(data[0]["guestIsPresent"], int)
    assert data[0]["guestIsPresent"] >= 0


async def test_get_by_id(ac: AsyncClient):
    table = await get_first()

    response = await ac.get(f"/api/tables/{table.id}")
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(table.id)
    assert data["num"] == table.num
    assert data["description"] == table.description
    assert data["maxGuests"] == table.max_guests
    assert data["guestsDef"] == table.guests_count
    assert data["guestsNow"] == table.guests_present_count

    assert data["guests"][0]["id"] == str(table.guests[0].id)
    assert data["guests"][0]["name"] == table.guests[0].name
    assert data["guests"][0]["isPresent"] == table.guests[0].is_present


async def test_get_guests_by_id(ac: AsyncClient):
    table = await get_first()

    response = await ac.get(f"/api/tables/{table.id}/guests")
    assert response.status_code == 200

    data = response.json()

    assert data[0]["id"] == str(table.guests[0].id)
    assert data[0]["name"] == table.guests[0].name
    assert data[0]["isPresent"] == table.guests[0].is_present


async def test_update(ac: AsyncClient):
    table = await get_first()

    update_data = {
        "description": "asd",
        "maxGuests": table.max_guests+5,
    }
    response = await ac.patch(f"/api/tables/{table.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()

    assert data["description"] == update_data["description"]
    assert data["maxGuests"] == update_data["maxGuests"]


async def test_get_by_id_not_found(ac: AsyncClient):
    response = await ac.get(f"/api/tables/{uuid.uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Table not found"


async def test_get_guests_by_id_not_found(ac: AsyncClient):
    response = await ac.get(f"/api/tables/{uuid.uuid4()}/guests")
    assert response.status_code == 404
    assert response.json()["detail"] == "Table not found"


async def test_update_not_found(ac: AsyncClient):
    response = await ac.patch(f"/api/tables/{uuid.uuid4()}", json={
        "description": "asd",
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Table not found"