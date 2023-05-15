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
    """Возвращает конкретный тип комнаты."""
    room = await RoomDAO.get_object(id=room_id)

    if not room:
        raise NotFoundException
    return room
