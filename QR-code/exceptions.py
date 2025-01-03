"""Модуль, содержащий исключения"""
class QRCodeError(Exception):
    """Базовый класс для ошибок QR-кода."""
    pass

class InvalidData(Exception):
    """Ошибка, вызываемая при недопустимых данных."""
    pass

class InvalidURL(Exception):
    """Ошибка, вызываемая при недопустимом URL."""
    pass

class InvalidShape(Exception):
    """Ошибка, вызываемая при недопустимой форме QR-кода."""
    pass

class InvalidColor(Exception):
    """Исключение для неверных цветов."""
    pass

