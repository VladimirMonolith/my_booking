from typing import List

from pydantic import BaseModel


class HotelRead(BaseModel):
    """Модель отображения отеля."""

    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int

    class Config:
        orm_mode = True


class HotelLocationRead(BaseModel):
    """Модель отображения отеля по заданным параметрам местоположения."""

    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    available_rooms: int
    image_id: int

    class Config:
        orm_mode = True


class HotelRoomsRead(BaseModel):
    """Модель отображения всех комнат отеля по заданным параметрам."""

    id: int
    name: str
    description: str
    price_per_day: int
    services: List[str]
    quantity: int
    available_rooms: int
    preliminary_cost: int
    image_id: int

    class Config:
        orm_mode = True
