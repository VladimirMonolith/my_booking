from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select, insert

from app.database.connection import async_session_maker


class BaseDAO:
    """Класс для работы с объектами БД."""

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
    async def get_object(cls, **kwargs):
        """Возвращает объект модели."""
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_all_objects_or_404(cls, **kwargs):
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

    @classmethod
    async def add_objects(cls, **kwargs):
        """Добавляет объекты в БД."""
        async with async_session_maker() as session:
            query = insert(cls.model).values(**kwargs)
            await session.execute(query)
            await session.commit()
