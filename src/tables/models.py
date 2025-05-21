import uuid

from sqlalchemy import UUID, Integer, String, Boolean, INTEGER, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class TableModel(Base):
    __tablename__ = "tables"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    num: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    max_guests: Mapped[int] = mapped_column(INTEGER, nullable=False)

    guests: Mapped[list["GuestModel"]] = relationship(
        "GuestModel",
        back_populates="table"
    )

    __table_args__ = (
        CheckConstraint("num > 0", name="num_positive"),
        CheckConstraint("max_guests > 0", name="max_guests_positive"),
    )