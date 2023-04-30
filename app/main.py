# import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.admin.models import BookingAdmin, HotelAdmin, RoomAdmin, UserAdmin
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin, ModelView
from app.bookings.router import router as bookings_router
from app.hotels.router import router as hotels_router
from app.images.router import router as images_router
from app.pages.router import router as pages_router
from app.rooms.router import router as rooms_router
from app.users.router import router as users_router
from app.config import settings
from app.database.connection import engine
from app.users.models import User



@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(
        f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}', encoding='utf8', decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    yield

app = FastAPI(lifespan=lifespan, title='my_booking')

app.mount('/static', StaticFiles(directory='app/static'), 'static')

app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(pages_router)
app.include_router(images_router)


# Подключение CORS, чтобы запросы к API могли приходить из браузера
origins = [
    # 3000 - порт, на котором работает фронтенд на React.js
    "http://localhost:3000",
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


admin = Admin(app, engine)

admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomAdmin)


# if __name__ == '__main__':
#     uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
