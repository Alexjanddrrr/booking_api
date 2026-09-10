from models.models import Booking
from schemas.shemas import CreateBookingSchema
from datetime import date, time

BOOKING_LOG: list[Booking] = []
AUTO_ID: int = 0


def check_slot_by_date_and_time(booking_date: date, booking_time: time) -> bool:
    """Проверяет, занят ли слот на указанную дату и время.

    :param
        booking_date: Дата бронирования.
        booking_time: Время бронирования.

    :return:
        True, если слот уже занят, иначе False.
    """
    for already_booked in BOOKING_LOG:
        if (already_booked.booking_date == booking_date
            and already_booked.booking_time == booking_time
            and already_booked.status == 'active'):
            return True

    return False


def create_booking_service(data: CreateBookingSchema) -> Booking:
    """Создаёт новую бронь, если слот свободен.

    :param
        data: Валидированные данные брони от клиента.

    :return:
        Созданная бронь со статусом 'active'.

    :raise:
        ValueError: Если слот на указанную дату/время уже занят.
    """
    global AUTO_ID

    if check_slot_by_date_and_time(data.booking_date, data.booking_time):
        raise ValueError('Этот слот уже занят')

    AUTO_ID += 1
    booking = Booking(id=AUTO_ID, **data.model_dump())
    BOOKING_LOG.append(booking)

    return booking


def get_bookings_service(date: date | None = None) -> list[Booking]:
    """Возвращает список броней, опционально отфильтрованный по дате.

    :param
        date: Дата для фильтрации. Если не указана — возвращаются все брони.

    :return:
        Список броней, соответствующих фильтру.
    """
    if date is None:
        return BOOKING_LOG

    return [booking_with_date
            for booking_with_date in BOOKING_LOG
            if booking_with_date.booking_date == date]


def get_booking_by_id_service(id: int) -> Booking:
    """Находит бронь по её id.

    :param
        id: Идентификатор брони.

    :return:
        Найденная бронь.

    :raise:
        ValueError: Если бронь с указанным id не найдена.
    """
    for booking in BOOKING_LOG:
        if booking.id == id:
            return booking
    raise ValueError(f'Бронь по номеру {id} не найдена')


def cancel_booking_by_id_service(id: int) -> Booking:
    """Отменяет бронь по id, не удаляя её физически.

    :param
        id: Идентификатор брони.

    :return:
        Отменённая бронь со статусом 'canceled'.

    :raise:
        ValueError: Если бронь с указанным id не найдена.
    """
    for booking in BOOKING_LOG:
        if booking.id == id:
            booking.status = 'canceled'
            return booking
    raise ValueError(f'Бронь по номеру {id} не найдена')