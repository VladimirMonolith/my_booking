from datetime import date

from sqlalchemy import select
from app.dao.base import BaseDAO
from app.database.connection import async_session_maker
from .models import Room


class RoomDAO(BaseDAO):
    model = Room

    # @classmethod
    # async def get_all_hotel_rooms_objects(
    #     cls, hotel_id: int,
    #     date_from: date, date_to: date
    # ):
    #     """Возвращает список всех номеров определенного отеля
    #     на конкретный промежуток времени."""

    #     async with async_session_maker() as session:
    #         query = select(Room).filter_by(hotel_id=hotel_id)
    #         all_hotels_rooms = await session.execute(query)
    #         return all_hotels_rooms.scalars().all()




