from typing import Optional

from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class Room(Base):
    """Модель комнаты."""

    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(length=150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(
        String(length=500), nullable=True
    )
    price_per_day: Mapped[int] = mapped_column(Integer, nullable=False)
    services: Mapped[str] = mapped_column(JSON, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    image_id: Mapped[int] = mapped_column(Integer, nullable=False)
    hotel = relationship('Hotel', back_populates='rooms')
    booking = relationship('Booking', back_populates='room')

    def __str__(self):
        return f'Комната: id - {self.id}, название - {self.name}'
