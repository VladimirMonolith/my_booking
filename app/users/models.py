from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.db import Base


class User(Base):
    """Модель пользователя."""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
