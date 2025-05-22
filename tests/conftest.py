import uuid
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.database import db
from src.models import Base
from src.config import settings
from src.main import app

engine_test = create_async_engine(settings.postgres_test_url, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        await session.commit()


app.dependency_overrides[db.get_async_session] = override_get_async_session


async def seeder_db():
    async with async_session_maker() as session:
        await session.execute(
            text(f"""
                    INSERT INTO tables (id, num, description, max_guests)
                    VALUES ('{uuid.uuid4()}', 1, 'Стол 1', 3),
                           ('{uuid.uuid4()}', 2, 'Стол 2', 2),
                           ('{uuid.uuid4()}', 3, 'Стол 3', 4),
                           ('{uuid.uuid4()}', 4, 'Стол 4', 4)
            """)
        )
        table_map = (await session.execute(text("""
                                            SELECT id, num
                                            FROM tables
                                            WHERE num IN (1, 2, 3, 4)
                                            """))).fetchall()
        table_id_by_num = {num: id_ for id_, num in table_map}

        guests_plan = {
            1: 2,
            2: 1,
            3: 3,
            4: 4,
        }

        full_names = [
            "Иванов Иван Иванович",
            "Петрова Мария Сергеевна",
            "Сидоров Алексей Николаевич",
            "Кузнецова Анна Владимировна",
            "Морозов Дмитрий Евгеньевич",
            "Васильева Ольга Павловна",
            "Смирнов Николай Артёмович",
            "Попова Елена Викторовна",
            "Михайлов Артём Алексеевич",
            "Фёдорова Анастасия Ивановна",
        ]

        guests = []
        name_index = 0

        for table_num, guest_count in guests_plan.items():
            table_id = table_id_by_num[table_num]
            for i in range(guest_count):
                if name_index >= len(full_names):
                    break
                guests.append({
                    "id": str(uuid.uuid4()),
                    "name": full_names[name_index],
                    "is_present": (i % 2 == 0),
                    "table_id": table_id
                })
                name_index += 1

        for guest in guests:
            await session.execute(
                text("""
                        INSERT INTO guests (id, name, is_present, table_id)
                        VALUES (:id, :name, :is_present, :table_id)
                        """),
                guest
            )

        await session.commit()


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await seeder_db()
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
