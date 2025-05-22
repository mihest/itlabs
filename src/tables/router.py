import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from pydantic import PositiveInt

from src.database import SessionDep
from src.tables.schemas import TableFilter, TableResponse, UpdateTable, TableGuestResponse, TableStatsResponse
from src.tables.service import TableService

router = APIRouter()
router_stats = APIRouter()


@router.get("",
            name="Retrieves the collection of Tables resources.",
            description="Retrieves the collection of Tables resources.")
async def get_list_tables(
        session: SessionDep,
        num: Optional[PositiveInt] = Query(None),
        num_list: Optional[list[PositiveInt]] = Query(None)
) -> list[TableResponse]:
    nums = set()

    if num:
        nums.add(num)
    if num_list:
        nums.update(num_list)

    filters = TableFilter(nums=nums)
    return await TableService.get_list(session, filters)


@router.get("/{table_id}",
            name="Retrieves a Table resource.",
            description="Retrieves a Table resource.")
async def get_table(
        table_id: uuid.UUID,
        session: SessionDep,
) -> TableResponse:
    return await TableService.get_by_id(session, table_id)


@router.patch("/{table_id}",
            name="Updates the Tables resource.",
            description="Updates the Tables resource.")
async def update_table(
        table_id: uuid.UUID,
        data: UpdateTable,
        session: SessionDep,
) -> TableResponse:
    return await TableService.update(session, table_id, data)


@router.get("/{table_id}/guests",
            name="Retrieves guests tables.",
            description="Retrieves guests tables.")
async def get_guests(
        table_id: uuid.UUID,
        session: SessionDep
) -> list[TableGuestResponse]:
    return await TableService.get_guests_by_id(session, table_id)


@router_stats.get("")
async def get_stats(
        session: SessionDep,
        num: Optional[PositiveInt] = Query(None),
        num_list: Optional[list[PositiveInt]] = Query(None)
) -> list[TableStatsResponse]:
    nums = set()

    if num:
        nums.add(num)
    if num_list:
        nums.update(num_list)

    filters = TableFilter(nums=nums)
    return await TableService.get_stats(session, filters)

