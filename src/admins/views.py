from fastapi import HTTPException

from sqladmin import ModelView
from sqlalchemy.exc import IntegrityError
from starlette.requests import Request

from src.guests.models import GuestModel
from src.tables.models import TableModel


class GuestAdmin(ModelView, model=GuestModel):
    name = "Гость"
    name_plural = "Гости"
    icon = "fa fa-user"

    column_list = [
        GuestModel.id,
        GuestModel.name,
        GuestModel.is_present,
        GuestModel.table,
    ]
    column_sortable_list = column_list
    column_editable_list = [
        GuestModel.name,
        GuestModel.is_present,
        GuestModel.table_id,
    ]
    column_searchable_list = [
        GuestModel.name,
        GuestModel.is_present,
        "table.num",
    ]
    column_default_sort = "table.num"
    column_details_list = column_list

    column_labels = {
        GuestModel.id: "ID",
        GuestModel.name: "ФИО",
        GuestModel.is_present: "Присутствие",
        GuestModel.table: "Стол",
        "table.num": "Номер стола",
    }


class TableAdmin(ModelView, model=TableModel):
    name = "Стол"
    name_plural = "Столы"
    icon = "fa fa-utensils"

    column_list = [
        TableModel.id,
        TableModel.num,
        TableModel.description,
        TableModel.max_guests,
        TableModel.guests_present_count,
        TableModel.guests_count,
    ]
    column_sortable_list = column_list
    column_default_sort = "num"
    column_editable_list = [
        TableModel.num,
        TableModel.description,
        TableModel.max_guests,
    ]
    column_searchable_list = [TableModel.num, TableModel.description]
    column_details_list = column_list
    form_excluded_columns = [TableModel.guests]

    column_labels = {
        TableModel.id: "ID",
        TableModel.num: "Номер стола",
        TableModel.description: "Описание",
        TableModel.max_guests: "Максимум гостей",
        TableModel.guests_count: "Гостей",
        TableModel.guests_present_count: "Присутствует гостей",
    }

    async def insert_model(self, request: Request, data: dict) -> None:
        try:
            return await super().insert_model(request, data)
        except Exception as e:
            if isinstance(e, IntegrityError):
                raise HTTPException(status_code=400, detail="Номер уже существует")
            raise e