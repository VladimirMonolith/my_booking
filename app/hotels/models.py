from sqlalchemy import JSON, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class Hotel(Base):
    """Модель отеля."""

    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(length=150), nullable=False)
    location: Mapped[str] = mapped_column(String(length=300), nullable=False)
    services: Mapped[str] = mapped_column(JSON, nullable=False)
    rooms_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id: Mapped[str] = mapped_column(Integer, nullable=False)
    rooms = relationship('Room', back_populates='hotel')

    def __str__(self):
        return f'Отель: id - {self.id}, название - {self.name}'
