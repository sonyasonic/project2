"""Модуль для валидации данных"""
from exceptions import InvalidData, InvalidURL, InvalidShape, InvalidColor

def validate_data(data):
    """Валидирует данные для QR-кода."""
    if not isinstance(data, str) or not data.strip():
        raise InvalidData("Данные должны быть непустой строкой.")

def validate_shape(shape):
    """Валидирует форму QR-кода."""
    if shape not in ['square', 'circle', 'rounded_square']:
        raise InvalidShape("Форма должна быть одной из: square, circle, rounded_square.")

def validate_url(url):
    """Валидирует URL фона."""
    if not isinstance(url, str):
        raise InvalidURL("Фоновый URL должен быть строкой.")
    if not url.startswith(('http://', 'https://')):
        raise InvalidURL("Недопустимый URL. Он должен начинаться с http:// или https://.")

def validate_color(color, color_map):
    """Валидирует цвет."""
    if color not in color_map:
        raise InvalidColor(f'Недопустимый цвет: {color}. Доступные цвета: {", ".join(color_map.keys())}')