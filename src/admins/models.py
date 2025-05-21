import uuid

from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class AdminModel(Base):
    __tablename__ = "admins"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100))
