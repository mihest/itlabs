import uuid

from sqlalchemy import UUID, Integer, String, INTEGER, CheckConstraint, func, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.guests.models import GuestModel
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

    def __str__(self) -> str:
        return f"Стол №{self.num}"

    @hybrid_property
    def guests_count(self):
        return len(self.guests)

    @guests_count.expression
    def guests_count(cls):
        return (
            select(func.count(GuestModel.id))
            .where(GuestModel.table_id == cls.id)
            .scalar_subquery()
        )

    @hybrid_property
    def guests_present_count(self):
        return sum(1 for g in self.guests if g.is_present)

    @guests_present_count.expression
    def guests_present_count(cls):
        return (
            select(func.sum(func.cast(GuestModel.is_present, Integer)))
            .where(GuestModel.table_id == cls.id)
            .scalar_subquery()
        )

