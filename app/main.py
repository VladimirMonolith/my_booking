# import uvicorn
from fastapi import FastAPI

from app.bookings.router import router as bookings_router
from app.hotels.router import router as hotels_router
from app.rooms.router import router as rooms_router
from app.users.router import router as users_router

app = FastAPI(title='my_booking')

app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(rooms_router)



# if __name__ == '__main__':
#     uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
