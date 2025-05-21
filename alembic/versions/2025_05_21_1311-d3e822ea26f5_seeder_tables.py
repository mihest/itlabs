"""seeder tables

Revision ID: d3e822ea26f5
Revises: 4c11aa8d0d8d
Create Date: 2025-05-21 13:11:19.177574

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic.
revision: str = 'd3e822ea26f5'
down_revision: Union[str, None] = '4c11aa8d0d8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    session = Session(bind=bind)

    session.execute(sa.text(f"""
                                INSERT INTO tables (id, num, description, max_guests)
                                VALUES ('{uuid.uuid4()}', 1, 'Стол 1', 3),
                                       ('{uuid.uuid4()}', 2, 'Стол 2', 2),
                                       ('{uuid.uuid4()}', 3, 'Стол 3', 4),
                                       ('{uuid.uuid4()}', 4, 'Стол 4', 4)
                                """))

    session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    session = Session(bind=bind)

    session.execute(sa.text("""
                                DELETE
                                FROM tables
                                WHERE num IN (1, 2, 3, 4)
                            """))
    session.commit()
