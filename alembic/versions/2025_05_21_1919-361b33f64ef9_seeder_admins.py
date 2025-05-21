"""seeder admins

Revision ID: 361b33f64ef9
Revises: 42df33738fc4
Create Date: 2025-05-21 19:19:25.792885

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

from src.admins.utils import get_password_hash

# revision identifiers, used by Alembic.
revision: str = '361b33f64ef9'
down_revision: Union[str, None] = '42df33738fc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    session = Session(bind=bind)

    session.execute(sa.text(f"""
                                    INSERT INTO admins (id, username, hashed_password)
                                    VALUES ('{uuid.uuid4()}', 'admin', '{get_password_hash('foo')}')
                                    """))

    session.commit()


def downgrade() -> None:
    """Downgrade schema."""
    pass
