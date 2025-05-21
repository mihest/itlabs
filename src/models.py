from sqlalchemy import MetaData, Integer, Column, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata = MetaData()


class Base(DeclarativeBase):
    metadata = metadata
