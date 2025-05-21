"""seeder guests

Revision ID: 0c94e6b8d1cf
Revises: d3e822ea26f5
Create Date: 2025-05-21 13:16:41.207024

"""
import  uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic.
revision: str = '0c94e6b8d1cf'
down_revision: Union[str, None] = 'd3e822ea26f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    session = Session(bind=bind)

    table_map = session.execute(sa.text("""
                                        SELECT id, num
                                        FROM tables
                                        WHERE num IN (1, 2, 3, 4)
                                        """)).fetchall()
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
        session.execute(
            sa.text("""
                    INSERT INTO guests (id, name, is_present, table_id)
                    VALUES (:id, :name, :is_present, :table_id)
                    """),
            guest
        )

    session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    session = Session(bind=bind)

    session.execute(sa.text("""
                            DELETE
                            FROM guests
                            WHERE name IN (
                                           'Иванов Иван Иванович',
                                           'Петрова Мария Сергеевна',
                                           'Сидоров Алексей Николаевич',
                                           'Кузнецова Анна Владимировна',
                                           'Морозов Дмитрий Евгеньевич',
                                           'Васильева Ольга Павловна',
                                           'Смирнов Николай Артёмович',
                                           'Попова Елена Викторовна',
                                           'Михайлов Артём Алексеевич',
                                           'Фёдорова Анастасия Ивановна'
                                )
                            """))
    session.commit()
