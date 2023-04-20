from datetime import date
from typing import List

from fastapi import APIRouter

from app.exceptions import NotFoundException

from .dao import RoomDAO
from .schemas import RoomRead

router = APIRouter(
    prefix='/rooms',
    tags=['rooms']
)


@router.get('', response_model=List[RoomRead])
async def get_all_rooms():
    """Возвращает все комнаты."""
    rooms = await RoomDAO.get_all_objects()

    if not rooms:
        raise NotFoundException
    return rooms


@router.get('/{room_id}', response_model=RoomRead)
async def get_room(room_id: int):
    """Возвращает конкретный тип комнаты по id."""
    room = await RoomDAO.get_object(id=room_id)

    if not room:
        raise NotFoundException
    return room


# @router.get('/{hotel_id}')
# async def get_all_hotel_rooms(hotel_id: int, date_from: date, date_to: date):
#     """Возвращает список всех номеров определенного отеля."""
#     return await RoomDAO.get_all_hotel_rooms_objects(
#         hotel_id=hotel_id,
#         date_from=date_from,
#         date_to=date_to
#     )
