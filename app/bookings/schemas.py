from datetime import date
from typing import List

from pydantic import BaseModel


class BookingRead(BaseModel):
    """Модель отображения бронирования."""

    id: int
    date_from: date
    date_to: date
    price_per_day: int
    total_days: int
    total_cost: int
    room_id: int
    user_id: int

    class Config:
        orm_mode = True


class BookingUserRead(BaseModel):
    """Модель отображения бронирования пользователя."""

    id: int
    date_from: date
    date_to: date
    price_per_day: int
    total_days: int
    total_cost: int
    user_id: int
    room_id: int
    name: str
    description: str
    services: List[str]
    image_id: str

    class Config:
        orm_mode = True
