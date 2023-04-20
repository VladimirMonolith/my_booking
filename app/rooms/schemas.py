from pydantic import BaseModel


class RoomRead(BaseModel):
    """Модель отображения комнаты."""

    id: int
    name: str
    description: str
    price_per_day: int
    services: list
    quantity: int
    hotel_id: int
    image_id: int

    class Config:
        orm_mode = True


# class HotelLocationRead(BaseModel):
#     """Модель отображения отеля по заданным параметрам местоположения."""

#     name: str
#     location: str
#     services: list
#     rooms_quantity: int
#     available_rooms: int

#     class Config:
#         orm_mode = True
