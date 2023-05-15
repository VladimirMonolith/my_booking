from typing import List

from pydantic import BaseModel


class RoomRead(BaseModel):
    """Модель отображения комнаты."""

    id: int
    name: str
    description: str
    price_per_day: int
    services: List[str]
    quantity: int
    hotel_id: int
    image_id: int

    class Config:
        orm_mode = True
