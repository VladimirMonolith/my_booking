# import uvicorn
from fastapi import FastAPI

from app.bookings.router import router as bookings_router

app = FastAPI(title='project')

app.include_router(bookings_router)


# if __name__ == '__main__':
#     uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
