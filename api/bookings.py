from fastapi import APIRouter, HTTPException
from schemas.shemas import CreateBookingSchema, BookingOutSchema
from models.models import Booking
from datetime import date
from services.booking_service import (
    create_booking_service,
    get_bookings_service,
    get_booking_by_id_service,
    cancel_booking_by_id_service
)

router = APIRouter()


@router.post('/bookings', status_code=201, response_model=BookingOutSchema)
def make_booking(data: CreateBookingSchema) -> Booking:
    """Создаёт новую бронь.

    :param
        data: Данные брони из тела запроса (валидируются Pydantic).

    :return:
        Созданная бронь с присвоенным id и статусом 'active'.

    :raise:
        HTTPException: 409, если слот на указанные дату/время уже занят.
    """
    try:
        booking = create_booking_service(data)
        return booking
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

@router.get('/bookings')
def get_bookings(date: date | None = None) -> list[Booking]:
    """Возвращает список броней.

    :param
        date: Опциональный фильтр по дате.

    :return:
        Список всех броней, либо отфильтрованных по дате.
    """
    return get_bookings_service(date)


@router.get('/bookings/{id}')
def get_booking_by_id(id: int) -> Booking:
    """Возвращает бронь по её id.

    :param
        id: Идентификатор брони.

    :return:
        Найденная бронь.

    :raise:
        HTTPException: 404, если бронь с указанным id не найдена.
    """
    try:
        return get_booking_by_id_service(id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.delete('/bookings/{id}')
def cancel_booking_by_id(id: int) -> Booking:
    """Отменяет бронь по id.

    Запись не удаляется физически, меняется только статус на 'canceled'.

    :param
        id: Идентификатор брони.

    :return:
        Отменённая бронь.

    :raise:
        HTTPException: 404, если бронь с указанным id не найдена.
    """
    try:
        return cancel_booking_by_id_service(id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))