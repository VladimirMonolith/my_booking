from app.dao.base import BaseDAO

from .models import Booking


class BookingDAO(BaseDAO):
    model = Booking
