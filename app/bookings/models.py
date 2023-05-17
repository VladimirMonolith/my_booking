from datetime import datetime

from sqlalchemy import Computed, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base
from app.rooms.models import Room
from app.users.models import User


class Booking(Base):
    """Модель бронирования."""

    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    date_from: Mapped[datetime] = mapped_column(Date, nullable=False)
    date_to: Mapped[datetime] = mapped_column(Date, nullable=False)
    price_per_day: Mapped[int] = mapped_column(Integer, nullable=False)
    total_days: Mapped[int] = mapped_column(
        Integer, Computed('date_to - date_from'), nullable=False
    )
    total_cost: Mapped[int] = mapped_column(
        Integer, Computed('(date_to - date_from) * price_per_day'),
        nullable=False
    )
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='booking')
    room: Mapped['Room'] = relationship(back_populates='booking')

    def __str__(self):
        return f'Бронирование: id - {self.id}, c {self.date_from} по {self.date_to}'
