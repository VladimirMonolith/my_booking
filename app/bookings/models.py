from datetime import datetime

from sqlalchemy import Computed, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.db import Base


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
