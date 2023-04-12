from datetime import datetime
from typing import List, Optional

from sqlalchemy import JSON, TIMESTAMP, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.db import Base


class Hotel(Base):
    """Модель отеля."""

    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(length=50), nullable=False)
    location: Mapped[str] = mapped_column(String(length=50), nullable=False)
    services: Mapped[list] = mapped_column(JSON)
    room_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id: Mapped[int] = mapped_column(Integer)
