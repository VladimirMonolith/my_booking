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
        """Добавляет объект бронирования в БД."""
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

            get_available_rooms = (
                    select(
                        (Room.quantity - func.count(booked_rooms.c.room_id))
                        .label('rooms_available')
                    )
                    .select_from(Room)
                    .join(
                        booked_rooms, booked_rooms.c.room_id == Room.id,
                        isouter=True
                    )
                    .where(Room.id == room_id)
                    .group_by(Room.quantity, booked_rooms.c.room_id)
                )

            rooms_available = await session.execute(get_available_rooms)
            rooms_available = rooms_available.scalar()

            if not rooms_available:
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

    @classmethod
    async def get_user_bookings_objects(cls, user_id: int):
        """Возвращает все бронирования текущего пользователя."""

        get_user_bookings = (
            select(
                Booking.id,
                Booking.date_from,
                Booking.date_to,
                Booking.price_per_day,
                Booking.total_days,
                Booking.total_cost,
                Booking.user_id,
                Booking.room_id,
                Room.name,
                Room.description,
                Room.services,
                Room.image_id
            )
            .join(
                Room,
                Booking.room_id == Room.id,
                isouter=True)
            .where(
                Booking.user_id == user_id
            )
        )

        async with async_session_maker() as session:
            user_bookings = await session.execute(get_user_bookings)
            return user_bookings.all()
