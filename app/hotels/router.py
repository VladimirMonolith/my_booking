from datetime import date, datetime, timedelta
from typing import List

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.exceptions import DateFromCannotBeAfterDateTo, NotFoundException

from .dao import HotelDAO
from .schemas import HotelRead, HotelRoomsRead

router = APIRouter(
    prefix='/hotels',
    tags=['hotels']
)


@router.get('', response_model=List[HotelRead])
async def get_all_hotels():
    """Возвращает все отели."""
    return await HotelDAO.get_all_objects()


@router.get('/{location}')
@cache(expire=60)
async def get_hotels_by_location(
    location: str,
    date_from: date = Query(
        ..., description=f'Например, {datetime.now().date()}'
    ),
    date_to: date = Query(
        ..., description=f'Например, {(datetime.now() + timedelta(days=7)).date()}'
    ),
):
    """Возвращает все отели по заданным параметрам местоположения."""
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    hotels = await HotelDAO.get_hotels_by_location_objects(
        location=location, date_from=date_from, date_to=date_to
    )

    if not hotels:
        raise NotFoundException
    return hotels


@router.get('/id/{hotel_id}', response_model=HotelRead)
async def get_hotel(hotel_id: int):
    """Возвращает конкретный отель по его id."""
    hotel = await HotelDAO.get_object(id=hotel_id)

    if not hotel:
        raise NotFoundException
    return hotel


@router.get('/{hotel_id}/rooms', response_model=List[HotelRoomsRead])
async def get_all_hotel_rooms(hotel_id: int, date_from: date, date_to: date):
    """Возвращает список всех/доступных номеров определенного отеля."""
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo

    return await HotelDAO.get_all_hotel_rooms_objects(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to
    )
