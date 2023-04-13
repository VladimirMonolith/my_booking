from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select

from app.database.connection import async_session_maker


class BaseDAO:
    """Класс для работы с объетами БД."""

    model = None

    @classmethod
    async def get_object_or_404(cls, **kwargs):
        """Возвращает объект модели или 404 ошибку."""
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            object = result.scalar_one_or_none()

            if not object:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail='Запрошенный объект не найден.'
                )
            return object

    @classmethod
    async def get_all_objects(cls, **kwargs):
        """Возвращает все объекты модели или 404 ошибку."""
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            objects = result.scalars().all()

            if not objects:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail='Данные не найдены.'
                )
            return objects
