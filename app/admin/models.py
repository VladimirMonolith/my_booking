from app.bookings.models import Booking
from app.hotels.models import Hotel
from app.rooms.models import Room
from sqladmin import ModelView

from app.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.booking]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'


class HotelAdmin(ModelView, model=Hotel):
    column_list = [c.name for c in Hotel.__table__.c] + [Hotel.rooms]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomAdmin(ModelView, model=Room):
    column_list = [c.name for c in Room.__table__.c] + [Room.hotel, Room.booking]
    name = "Номер"
    name_plural = "Номера"
    icon = "fa-solid fa-bed"



class BookingAdmin(ModelView, model=Booking):
    column_list = [c.name for c in Booking.__table__.c] + [Booking.user]
    name = 'Бронирование'
    name_plural = 'Бронирования'
    icon = "fa-solid fa-book"

