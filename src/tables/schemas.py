import uuid
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class TableFilter(BaseModel):
    nums: set[int]


class TableGuestResponse(BaseModel):
    id: uuid.UUID
    name: str
    isPresent: bool


class TableResponse(BaseModel):
    id: uuid.UUID
    num: int
    description: str
    maxGuests: int
    guestsDef: int
    guestsNow: int
    guests: list[TableGuestResponse]


class TableStatsResponse(BaseModel):
    id: uuid.UUID
    num: int
    maxGuests: int
    booking: int
    guestIsPresent: int

class UpdateTable(BaseModel):
    num: Optional[PositiveInt] = None
    description: Optional[str] = None
    max_guests: Optional[PositiveInt] = Field(None, alias="maxGuests")