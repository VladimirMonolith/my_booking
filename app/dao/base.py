from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import async_session_maker
from app.exceptions import NotFoundException
from app.logger import logger


class BaseDAO:
    """Класс для работы с объектами БД."""

    model = None

    @classmethod
    async def get_all_objects(cls, **kwargs):
        """Возвращает все объекты модели."""
        async with async_session_maker() as session:
            query = (select(cls.model.__table__.columns).filter_by(**kwargs)
                     .order_by(cls.model.id))
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def get_object(cls, **kwargs):
        """Возвращает объект модели."""
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**kwargs)
            result = await session.execute(query)
            return result.mappings().one_or_none()

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

    @classmethod
    async def add_objects(cls, *data):
        """Добавляет объекты в БД."""
        try:
            query = insert(cls.model).values(*data).returning(cls.model.id)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                message = 'Database Exception'
            elif isinstance(error, Exception):
                message = 'Unknown Exception'
            message += ': Cannot bulk insert data into table'

            logger.error(
                message,
                extra={'table': cls.model.__tablename__},
                exc_info=True
            )
            return None
