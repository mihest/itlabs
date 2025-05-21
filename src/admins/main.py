from fastapi.responses import RedirectResponse
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from pydantic import BaseModel
from sqlalchemy import select

from src.admins.models import AdminModel
from src.admins.utils import is_valid_password
from src.admins.views import GuestAdmin, TableAdmin
from src.database import db


class UserIn(BaseModel):
    username: str
    password: str


class MyAuthenticationBackend(AuthenticationBackend):
    async def login(self, request):
        form = await request.form()
        username, password = form["username"], form["password"]

        async with db.session() as session:
            stmt = select(AdminModel).where(AdminModel.username == username)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

        if not user or not is_valid_password(password, user.hashed_password):
            return False

        request.session.update({"user_id": str(user.id)})
        return True

    async def logout(self, request):
        request.session.clear()
        return True

    async def authenticate(self, request):
        is_auth = request.session.get("user_id")
        if not is_auth:
            return RedirectResponse("/admin/login")
        return True


def init_admin(app):
    admin = Admin(app=app, engine=db.engine, authentication_backend=MyAuthenticationBackend(
        secret_key="SUPER_SECRET_KEY"
    ))
    admin.add_view(TableAdmin)
    admin.add_view(GuestAdmin)