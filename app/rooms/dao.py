from app.dao.base import BaseDAO

from .models import Room


class RoomDAO(BaseDAO):
    model = Room
