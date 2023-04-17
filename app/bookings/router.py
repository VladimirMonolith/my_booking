from typing import List

from fastapi import APIRouter, Depends, Request
from app.users.dependencies import get_current_user

from app.users.models import User

from .dao import BookingDAO
from .schemas import BookingRead

router = APIRouter(
    prefix='/bookings',
    tags=['bookings']
)

# @router.get('', response_model=List[BookingRead])
# async def get_bookings():
#     """Возвращает все бронирования."""
#     return await BookingDAO.get_all_objects_or_404()

@router.get('', response_model=List[BookingRead])
async def get_bookings(user: User = Depends(get_current_user)):
    """Возвращает все бронирования."""
    return await BookingDAO.get_all_objects(user_id=user.id)


@router.get('/{booking_id}', response_model=BookingRead)
async def get_booking(booking_id: int):
    """Возвращает конкретное бронирование."""
    return await BookingDAO.get_object_or_404(id=booking_id)
