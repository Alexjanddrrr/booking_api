from pydantic import BaseModel, field_validator, Field
from datetime import date, time, timedelta

from core.config import TIME_SLOTS


class CreateBookingSchema(BaseModel):
    """Данные для создания новой брони столика."""
    name: str = Field(
        min_length=2,
        max_length=30,
        pattern=r'^[a-zA-Zа-яА-ЯёЁ]+([\s\-][a-zA-Zа-яА-ЯёЁ]+)*$',
        description='Имя гостя. Минимум 2 символа, только буквы, пробелы, дефис.',
        examples=['Иван Иванов']
    )
    phone: str = Field(
        pattern=r'^8\d{10}$',
        description='Телефон в формате +7XXXXXXXXXX или 8XXXXXXXXXX.',
        examples=['+79261234567']
    )
    booking_date: date = Field(
        description='Дата брони: не раньше сегодня и не позднее +90 дней.',
        examples=['2026-08-20']
    )
    booking_time: time  = Field(
        description='Время брони: слоты с 12:00 до 22:00 с шагом 1 час.',
        examples=['14:00:00']
    )
    guests: int = Field(
        ge=1,
        le=12,
        description='Количество гостей: от 1 до 12.',
        examples=[2])

    @field_validator('phone', mode='before')
    @classmethod
    def phone_normalize(cls, value: str) -> str:
        """Приводит номер к единому формату 8XXXXXXXXXX."""
        if value.startswith('+7'):
            return '8' + value[2:]
        return value

    @field_validator('booking_date')
    @classmethod
    def check_date(cls, value: date) -> date:
        """Проверяет, что дата не раньше сегодня и не позже +90 дней."""
        today = date.today()
        if value < today:
            raise ValueError('Дата брони не может быть раньше сегодняшнего дня')
        if value > today + timedelta(days=90):
            raise ValueError('Дата брони не может быть больше, чем 90 дней')
        return value

    @field_validator('booking_time')
    @classmethod
    def check_time(cls, value: time) -> time:
        """Проверяет, что время попадает в допустимые часовые слоты."""
        if value in TIME_SLOTS:
            return value
        raise ValueError('Доступны слоты с 12:00 до 22:00 с шагом в 1 час')


class BookingOutSchema(CreateBookingSchema):
    """Бронь, возвращаемая клиенту: с id и текущим статусом."""
    id: int = Field(description='Уникальный идентификатор брони.')
    status: str  = Field(description="Статус брони: 'active' или 'canceled'.")