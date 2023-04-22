from datetime import date

from sqlalchemy import select

from app.dao.base import BaseDAO
from app.database.connection import async_session_maker

from .models import Room


class RoomDAO(BaseDAO):
    model = Room
