from datetime import date
from typing import List, Union

from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

from app.exceptions import NotFoundException
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import User

from .dao import BookingDAO
from .schemas import BookingRead, BookingUserRead

router = APIRouter(
    prefix='/bookings',
    tags=['bookings']
)


# @router.post('', response_model=BookingRead)
# async def add_booking(
#     room_id: int,
#     date_from: date,
#     date_to: date,
#     user: User = Depends(get_current_user),
# ):
#     """Позволяет добавить бронирование."""
#     return await BookingDAO.add_booking_object(
#         user_id=user.id, room_id=room_id,
#         date_from=date_from, date_to=date_to
#     )

@router.post('')
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: User = Depends(get_current_user),
):
    """Позволяет добавить бронирование."""
    booking = await BookingDAO.add_booking_object(
        user_id=user.id, room_id=room_id,
        date_from=date_from, date_to=date_to
    )
    booking_dict = parse_obj_as(BookingRead, booking).dict()
    send_booking_confirmation_email.delay(booking=booking_dict, email_to=user.email)

    return booking_dict




@router.get('', response_model=Union[List[BookingUserRead], str])
async def get_user_bookings(user: User = Depends(get_current_user)):
    """Возвращает все бронирования текущего пользователя."""
    user_bookings = await BookingDAO.get_user_bookings_objects(user_id=user.id)

    if not user_bookings:
        return 'У Вас пока нет бронирований.'
    return await BookingDAO.get_user_bookings_objects(user_id=user.id)


@router.get('/{booking_id}', response_model=BookingRead)
async def get_booking(booking_id: int):
    """Возвращает бронирование по id."""
    booking = await BookingDAO.get_object(id=booking_id)

    if not booking:
        raise NotFoundException
    return booking


@router.delete('/{booking_id}')
async def delete_booking(
    booking_id: int, user: User = Depends(get_current_user)
):
    """Удаляет конкретное бронирование пользователя."""
    return await BookingDAO.delete_object(
        id=booking_id, user_id=user.id
    )
