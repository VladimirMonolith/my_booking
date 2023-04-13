from typing import List

from fastapi import APIRouter

from .dao import BookingDAO
from .schemas import BookingRead

router = APIRouter(
    prefix='/bookings',
    tags=['bookings']
)

@router.get('', response_model=List[BookingRead])
async def get_bookings():
    """Возвращает все бронирования."""
    return await BookingDAO.get_all_objects_or_404()


@router.get('/{booking_id}', response_model=BookingRead)
async def get_booking(booking_id: int):
    """Возвращает конкретное бронирование."""
    return await BookingDAO.get_object_or_404(id=booking_id)
