from dataclasses import dataclass
from datetime import date, time


@dataclass
class Booking:
    """Доменная модель брони столика, хранящаяся в системе.

    :param:
        id: Уникальный идентификатор брони.
        name: Имя гостя.
        phone: Телефон гостя в формате 8XXXXXXXXXX.
        booking_date: Дата брони.
        booking_time: Время брони.
        guests: Количество гостей.
        status: Статус брони: 'active' или 'canceled'.
    """

    id: int
    name: str
    phone: str
    booking_date: date
    booking_time: time
    guests: int
    status: str = 'active'