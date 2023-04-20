from datetime import date
from typing import List

from fastapi import APIRouter

from app.rooms.dao import RoomDAO
from app.rooms.schemas import RoomRead

from .dao import HotelDAO
from .schemas import HotelLocationRead, HotelRead, HotelRoomsRead

router = APIRouter(
    prefix='/hotels',
    tags=['hotels']
)


@router.get('', response_model=List[HotelRead])
async def get_all_hotels():
    """Возвращает все отели."""
    return await HotelDAO.get_all_objects()


@router.get('/{location}', response_model=List[HotelLocationRead])
async def get_hotels_by_location(
    location: str,
    date_from: date,
    date_to: date
):
    """Возвращает все отели по заданным параметрам местоположения."""
    return await HotelDAO.get_hotels_by_location_objects(
        location=location, date_from=date_from, date_to=date_to
    )


@router.get('/{hotel_id}/rooms', response_model=List[HotelRoomsRead])
async def get_all_hotel_rooms(hotel_id: int, date_from: date, date_to: date):
    """Возвращает список всех номеров определенного отеля."""
    return await HotelDAO.get_all_hotel_rooms_objects(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to
    )
