import uuid

from sqlalchemy import UUID, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base
from src.tables.models import TableModel


class GuestModel(Base):
    __tablename__ = "guests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name: Mapped[str] = mapped_column(String, nullable=False)
    isPresent: Mapped[bool] = mapped_column(Boolean, nullable=False)
    table_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tables.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )

    table: Mapped[TableModel] = relationship(
        "TableModel",
        back_populates="guests"
    )