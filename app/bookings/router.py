from datetime import date
from typing import List

from fastapi import APIRouter, Depends

from app.users.dependencies import get_current_user
from app.users.models import User

from .dao import BookingDAO
from .schemas import BookingRead

router = APIRouter(
    prefix='/bookings',
    tags=['bookings']
)


@router.get('', response_model=List[BookingRead])
async def get_bookings(user: User = Depends(get_current_user)):
    """Возвращает все бронирования текущего пользователя."""
    return await BookingDAO.get_all_objects(user_id=user.id)


@router.post('', response_model=BookingRead)
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: User = Depends(get_current_user),
):
    """Позволяет добавить бронирование."""
    return await BookingDAO.add_booking_object(
        user_id=user.id, room_id=room_id,
        date_from=date_from, date_to=date_to
    )


@router.get('/{booking_id}', response_model=BookingRead)
async def get_booking(booking_id: int):
    """Возвращает конкретное бронирование."""
    return await BookingDAO.get_object(id=booking_id)
