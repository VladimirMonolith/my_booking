from datetime import date

from sqlalchemy import and_, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.database.connection import async_session_maker
from app.exceptions import RoomCantBookedException
from app.logger import logger
from app.rooms.models import Room

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
        try:
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
                ).returning(
                    Booking.id, Booking.date_from, Booking.date_to,
                    Booking.price_per_day, Booking.total_days,
                    Booking.total_cost, Booking.room_id,
                    Booking.user_id
                )

                # ).returning(Booking)

                new_booking = await session.execute(add_booking)
                await session.commit()
                # return new_booking.scalar()
                return new_booking.mappings().one()

        except RoomCantBookedException:
            raise RoomCantBookedException

        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                message = 'Database Exception'
            elif isinstance(error, Exception):
                message = 'Unknown Exception'
            message += ': Невозможно добавить бронирование'
            extra = {
                'user_id': user_id,
                'room_id': room_id,
                'date_from': date_from,
                'date_to': date_to,
            }
            logger.error(message, extra=extra, exc_info=True)

    @classmethod
    async def get_user_bookings_objects(cls, user_id: int):
        """Возвращает все бронирования текущего пользователя."""
        async with async_session_maker() as session:
            get_user_bookings = (
                select(
                    Booking.__table__.columns,
                    Room.__table__.columns
                )
                .join(
                    Room,
                    Booking.room_id == Room.id,
                    isouter=True)
                .where(
                    Booking.user_id == user_id
                )
            )

            user_bookings = await session.execute(get_user_bookings)
            return user_bookings.mappings().all()
