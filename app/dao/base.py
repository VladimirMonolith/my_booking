from sqlalchemy import insert, select

from app.database.connection import async_session_maker
from app.exceptions import NotFoundException


class BaseDAO:
    """Класс для работы с объектами БД."""

    model = None

    @classmethod
    async def get_all_objects(cls, **kwargs):
        """Возвращает все объекты модели."""
        async with async_session_maker() as session:
            query = (select(cls.model).filter_by(**kwargs)
                     .order_by(cls.model.id))
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_object(cls, **kwargs):
        """Возвращает объект модели."""
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add_object(cls, **kwargs):
        """Добавляет объект в БД."""
        async with async_session_maker() as session:
            query = insert(cls.model).values(**kwargs)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_object(cls, **kwargs):
        """Удаляет объект из БД."""
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            result = result.scalar()

            if not result:
                raise NotFoundException
            await session.delete(result)
            await session.commit()
            return 'Удаление успешно завершено.'
