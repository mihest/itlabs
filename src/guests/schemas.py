import uuid
from typing import Optional

from pydantic import BaseModel, Field


class GuestFilter(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    is_present: Optional[bool] = Field(None, alias="isPresent")


class GuestTableResponse(BaseModel):
    id: uuid.UUID
    num: int
    description: str
    max_guests: int = Field(..., alias="maxGuests")
    guests_def: int = Field(..., alias="guestsDef")
    guests_now: int = Field(..., alias="guestsNow")



class GuestResponse(BaseModel):
    id: uuid.UUID
    name: str
    is_present: bool = Field(None, alias="isPresent")
    table: GuestTableResponse

class UpdateGuest(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    is_present: Optional[bool] = Field(None, alias="isPresent")
    table_id: Optional[uuid.UUID] = Field(None, alias="tableId")
