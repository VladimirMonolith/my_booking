from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import BookingRead
from app.database.connection import get_async_session

from .models import Booking
from .dao import BookingDAO


router = APIRouter(
    prefix='/bookings',
    tags=['bookings']
)

@router.get('', response_model=List[BookingRead])
async def get_bookings():
    """Возвращает все бронирования."""
    return await BookingDAO.get_all_objects()

    


@router.get('/{booking_id}', response_model=BookingRead)
async def get_booking(booking_id: int):
    """Возвращает конкретное бронирование."""
    return await BookingDAO.get_object_or_404(id=booking_id)
