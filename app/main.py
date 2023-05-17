# import uvicorn
import time
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.models import BookingAdmin, HotelAdmin, RoomAdmin, UserAdmin
from app.bookings.router import router as bookings_router
from app.config import settings
from app.database.connection import engine
from app.hotels.router import router as hotels_router
from app.images.router import router as images_router
from app.import_data.router import router as import_data_router
from app.logger import logger
from app.pages.router import router as pages_router
from app.prometheus.router import router as prometheus_router
from app.rooms.router import router as rooms_router
from app.users.router import router as users_router




@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(
        f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}',
        encoding='utf8',
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    yield

app = FastAPI(lifespan=lifespan, title='my_booking')
# app = FastAPI(title='my_booking')

sentry_sdk.init(
    dsn='https://b6decba048b34e27913119ed94a07ef6@o1384117.ingest.sentry.io/4505118588600320',
    traces_sample_rate=1.0,
)


app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(pages_router)
app.include_router(images_router)
app.include_router(import_data_router)
app.include_router(prometheus_router)


origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=[
        'Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers',
        'Access-Control-Allow-Origin', 'Authorization'
    ],
)


app = VersionedFastAPI(
    app,
    version_format='{major}',
    prefix_format='/v{major}',
)

# app.include_router(pages_router)


@app.on_event("startup")
def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=['.*admin.*', '/metrics'],
)
instrumentator.instrument(app).expose(app)


admin = Admin(app, engine)

admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomAdmin)

app.mount('/static', StaticFiles(directory='app/static'), 'static')

# @app.middleware('http')
# async def add_process_time_header(request: Request, call_next):
#     """Добавляет заголовок со временем выполнения запроса."""
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     logger.info(
#         'Request handlinf time',
#         extra={'process_time': round(process_time, 4)}
#     )
#     return response

# if __name__ == '__main__':
#     uvicorn.run('app.main:app', host='127.0.0.1', port=8000, reload=True)
