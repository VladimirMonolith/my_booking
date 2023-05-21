# Cервис My_booking

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![fastapi-users](https://img.shields.io/badge/-fastapi--users-464646?style=flat-square&logo=fastapi--users)](https://fastapi-users.github.io/fastapi-users/)
[![Асинхронность](https://img.shields.io/badge/-Асинхронность-464646?style=flat-square&logo=Асинхронность)]()
[![Anyio](https://img.shields.io/badge/-Anyio-464646?style=flat-square&logo=Anyio)](https://anyio.readthedocs.io/en/stable/)
[![Cookies](https://img.shields.io/badge/-Cookies-464646?style=flat-square&logo=Cookies)]()
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat-square&logo=JWT)]()
[![Alembic](https://img.shields.io/badge/-Alembic-464646?style=flat-square&logo=Alembic)](https://alembic.sqlalchemy.org/en/latest/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat-square&logo=SQLAlchemy)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/-Redis-464646?style=flat-square&logo=Redis)](https://redis.io/)
[![Celery](https://img.shields.io/badge/-Celery-464646?style=flat-square&logo=Celery)](https://docs.celeryq.dev/en/stable/)
[![Uvicorn](https://img.shields.io/badge/-Uvicorn-464646?style=flat-square&logo=gunicorn)](https://www.uvicorn.org/)

## Описание

Cервис Filegram и API для него.Интегрирован асинхронный подход к запросам к БД.Пользователи могут загружать медиаконтент(изображения, видео, аудио) и просматривать/прослушивать его в медиаплеере.Для кеширования использован Redis.Для фоновых задач подключён Celery.Реализована возможность чата посредством вебсокетов.Проект подготовлен для развертывания в Docker-контейнерах.

### Доступный функционал

- Аутентификация реализована с помощью куков и JWT-токена.
- У неаутентифицированных пользователей доступ к API только на уровне чтения.
- Создание объектов разрешено только аутентифицированным пользователям, прошедшим верификацию.
- Управление пользователями доступно при наличии прав суперпользователя.
- Возможность получения подробной информации о себе и ее редактирование, если пользователь прошел верификацию.
- Получение списка всего доступного контента.
- Возможность загрузки медиаконтента.
- Получение, обновление и удаление конкретного файла.
- Просмотр контента в плеере с возможностью выбрать необходимую стартовую точку воспроизведения.
- Пользователь может получить на свой email отчет о количестве загрузок.
- Онлайн-чат

#### Документация к API доступна по адресу <http://localhost:8000/docs/> после локального запуска проекта

#### Технологи

- Python 3.9
- FastAPI 0.92.0
- fasapi-users 10.4.1
- fastapi-cache2 0.2.1
- Asynchronous
- Anyio
- Cookies
- JWT
- Alembic
- SQLAlchemy 2.0.4
- Docker
- PostgreSQL
- Redis 4.5.2
- Celery 5.2.7
- Flower
- Asyncpg
- Uvicorn
- CORS

#### Локальный запуск проекта

- Преварительно необходимо установить Docker для вашей системы.

- Склонировать репозиторий:

```bash
   git clone <название репозитория>
```

Cоздать и активировать виртуальное окружение:

Команды для установки виртуального окружения на Mac или Linux:

```bash
   python3 -m venv env
   source env/bin/activate
```

Команды для Windows:

```bash
   python -m venv venv
   source venv/Scripts/activate
```

- Перейти в директорию infra:

```bash
   cd source/infra
```

- Создать файл .env по образцу:

```bash
   cp .env.example .env
```

- Выполнить команду для запуска БД PostgreSQL в Docker-контейнере:

```bash
   docker-compose up 
```

- Установить зависимости из файла requirements.txt:

```bash
   cd ..
   cd ..
   pip install -r requirements.txt
```

- Для создания миграций выполнить команду:

```bash
   alembic init migrations
```

- В alembic.ini нужно задать адрес базы данных.

```bash
   sqlalchemy.url = postgresql+asyncpg://%(POSTGRES_USER)s:%(POSTGRES_PASSWORD)s@%(POSTGRES_HOST)s:%(POSTGRES_PORT)s/%(POSTGRES_DB_NAME)s?async_fallback=True
```

- В папке migrations в env файле должны быть следующие импорты:

```bash
from alembic import context

from source.infra.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB_NAME
```

- В этом же файле добавить получение переменных из конфига:

```bash
config = context.config

section = config.config_ini_section
config.set_section_option(section, "POSTGRES_USER", POSTGRES_USER)
config.set_section_option(section, "POSTGRES_PASSWORD", POSTGRES_PASSWORD)
config.set_section_option(section, "POSTGRES_HOST", POSTGRES_HOST)
config.set_section_option(section, "POSTGRES_PORT", POSTGRES_PORT)
config.set_section_option(section, "POSTGRES_DB_NAME", POSTGRES_DB_NAME)
```

- В этом же файле добавить импорт моделей и установку метадаты в блоке, где написано from myapp import mymodel:

```bash
from source.database.models import Base
target_metadata = Base.metadata
```

- Инициализировать БД:

``` bash
    alembic revision --autogenerate -m "comment"  
```

- Применить миграцию:

``` bash
    alembic upgrade heads  
```

- Перейти в директорию source:

``` bash
    cd source   
```

- Запустить проект:

``` bash
    uvicorn main:app --reload   
```

#### Примеры некоторых запросов API

Регистрация пользователя:

```bash
   POST /auth/register
```

Получение токена верификации:

```bash
   POST /auth/request-verify-token
```

Сброс пароля:

```bash
   POST /auth/reset-password
```

Получение данных своей учетной записи:

```bash
   GET /users/me 
```

Удаление пользователя:

```bash
   DELETE /users/id
```

Добавление контента:

```bash
   POST /contents/
```

Обновление контента:
  
```bash
   PATCH /contents/content_id
```

Просмотр контента в плеере:

```bash
   GET /contents/streamig/content_id
```

#### Полный список запросов API находятся в документации

#### Автор

Гут Владимир - [https://github.com/VladimirMonolith](http://github.com/VladimirMonolith)
