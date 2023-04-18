from datetime import date

from fastapi import Depends
from sqlalchemy import and_, func, insert, or_, select

from app.dao.base import BaseDAO
from app.database.connection import async_session_maker
from app.exceptions import RoomCantBookedException
from app.rooms.models import Room
from app.users.dependencies import get_current_user
from app.users.models import User

from .models import Booking


class BookingDAO(BaseDAO):
    model = Booking

    @classmethod
    async def add_booking_object(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date
    ):
        """Добавляет объекты бронирования в БД."""
        async with async_session_maker() as session:
            booked_rooms = select(Booking).where(
                and_(
                    Booking.room_id == room_id,
                    or_(
                        and_(
                            Booking.date_from >= date_from,
                            Booking.date_from <= date_to
                        ),
                        and_(
                            Booking.date_from <= date_from,
                            Booking.date_to > date_from
                        )           
                    )
                )
            ).cte('booked_rooms')

            get_rooms_left = (
                    select(
                        (Room.quantity - func.count(booked_rooms.c.room_id))
                        .label('rooms_left')
                    )
                    .select_from(Room)
                    .join(
                        booked_rooms, booked_rooms.c.room_id == Room.id,
                        isouter=True
                    )
                    .where(Room.id == room_id)
                    .group_by(Room.quantity, booked_rooms.c.room_id)
                )
            
            rooms_left = await session.execute(get_rooms_left)
            rooms_left = rooms_left.scalar()

            if not rooms_left:
                raise RoomCantBookedException
            
            get_room_price = select(
                Room.price_per_day
            ).filter_by(id=room_id)
            price = await session.execute(get_room_price)
            price = price.scalar()
            add_booking = insert(Booking).values(
                user_id=user_id,
                room_id=room_id,
                date_from=date_from,
                date_to=date_to,
                price_per_day=price
            ).returning(Booking)

       
            new_booking = await session.execute(add_booking)
            await session.commit()
            return new_booking.scalar()



        

