from datetime import time

# Допустимые слоты бронирования: с 12:00 до 22:00 с шагом в 1 час
TIME_SLOTS: set[time] = {time(hour, 0) for hour in range(12, 23)}