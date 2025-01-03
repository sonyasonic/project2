"""Модуль для генерации QR-кода с заданными параметрами (форма, цвет, фон)"""
import qrcode
import requests
from PIL import Image, ImageDraw
from io import BytesIO
from validation import validate_data, validate_shape, validate_url, validate_color
from exceptions import InvalidData, InvalidURL, InvalidShape, InvalidColor

# Определяем стандартные и дополнительные цвета
COLOR_MAP = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "pink": (255, 192, 203),
    "teal": (0, 128, 128),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
}

class QRCodeGenerator:
    """Класс для генерации QR-кода с параметрами цвета и формы."""

    def __init__(self, data: str, shape: str):
        """Инициализация QR-кода с данными и формой."""
        # Проверка типа данных и формы
        if not isinstance(data, str):
            raise TypeError("Данные должны быть строкой.")
        if not isinstance(shape, str):
            raise TypeError("Форма должна быть строкой.")

        # Валидация данных и формы с использованием функций из модуля validation
        validate_data(data)
        validate_shape(shape)
        self.data = data
        self.shape = shape

    @staticmethod
    def get_color(prompt: str):
        """Функция для определения цвета QR-кода и цвета его фона
        Args:
            prompt (str): Сообщение для пользователя, запрашивающее цвет."""
        # Проверка типа данных prompt
        if not isinstance(prompt, str):
            raise TypeError("prompt должен быть строкой.")
        print("Доступные цвета: ", ", ".join(COLOR_MAP.keys()))  # Разрешенные цвета для пользователя
        while True:
            user_input = input(prompt).strip()
            color = user_input.lower()
            try:
                validate_color(color, COLOR_MAP) # Валидация цвета
                return color
            except InvalidColor as e:
                print("Ошибка:", e)

    def generate_qr_image(self, fill_color="black", back_color="white"):
        """Функция генерирует QR-код и возвращает изображение с заданной формой."""

        # Создание объекта QR-кода
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4.5,
        )
        qr.add_data(self.data)
        qr.make(fit=True)

        # Создание изображения QR-кода, конвертируя в формат RGBA для прозрачности
        qr_image = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")
        # Применение формы к QR-коду
        if self.shape == 'circle':
            qr_image = self.add_circle_shape(qr_image)
        elif self.shape == 'rounded_square':
            qr_image = self.add_rounded_square_shape(qr_image)

        print("QR-код успешно сгенерирован.")
        return qr_image

    def add_circle_shape(self, image):
        """Изменяет форму изображения QR-кода на круг."""
        # Проверяем, что аргумент 'image' является экземпляром PIL.Image.Image
        if not isinstance(image, Image.Image):
            raise TypeError("Аргумент 'image' должен быть экземпляром PIL.Image.Image.")
        mask = Image.new('L', image.size, 0) # Создаем маску того же размера, что и QR-код, заполненную нулями (черный цвет).
        draw = ImageDraw.Draw(mask) # Создаем объект ImageDraw для рисования на маске.
        draw.ellipse((0, 0, image.size[0], image.size[1]), fill=255) # Рисуем эллипс на маске, который будет круглым, заполняя его белым цветом (255)
        image.putalpha(mask) # Применяем маску к изображению QR-кода.
        return image

    def add_rounded_square_shape(self, image):
        """Изменяет форму изображения QR-кода на закругленный квадрат."""
        # Проверяем, что аргумент 'image' является экземпляром PIL.Image.Image
        if not isinstance(image, Image.Image):
            raise ValueError("Аргумент 'image' должен быть экземпляром PIL.Image.Image.")
        radius = 20  # Радиус закругления углов
        mask = Image.new('L', image.size, 0) # Создаем маску того же размера, что и QR-код, заполненную нулями (черный цвет)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, image.size[0], image.size[1]), radius=radius, fill=255) # Рисуем закругленный прямоугольник на маске, заполняя его белым цветом (255)
        image.putalpha(mask) # Применяем маску к изображению QR-кода.
        return image

class QRCodeWithBackground:
    """Класс для добавления фонового изображения к QR-коду."""

    def __init__(self, qr_image: Image.Image, background_url: str):
        """Инициализация объекта с QR-кодом и URL фонового изображения."""
        # Проверка типа данных для qr_image
        if not isinstance(qr_image, Image.Image):
            raise TypeError("Аргумент 'qr_image' должен быть экземпляром PIL.Image.Image.")
        # Проверка типа данных для background_ur
        if not isinstance(background_url, str):
            raise TypeError("Аргумент 'background_url' должен быть строкой.")
        # Валидация URL фонового изображения
        validate_url(background_url)
        self.qr_image = qr_image
        self.background_url = background_url

    def fetch_background(self):
        """Скачивает фоновое изображение."""
        try:
            response = requests.get(self.background_url) # Отправка GET-запроса по указанному URL
            if response.status_code != 200: # Проверка, что запрос успешен (код 200)
                raise InvalidURL("Не удалось загрузить изображение фона.")
            return Image.open(BytesIO(response.content))
        except Exception as e:
            raise InvalidURL(f"Ошибка при загрузке изображения: {e}")

    def apply_background(self):
        """Применяет фоновое изображение к QR-коду."""

        background = self.fetch_background() # Получение фонового изображения

        # Вычисление ширины и высоты фона с учетом размера QR-кода
        bg_width = int(self.qr_image.size[0] * 1.5)
        bg_height = int(self.qr_image.size[1] * 1.5)

        background = background.resize((bg_width, bg_height), Image.LANCZOS) # Изменение размера фонового изображения

        # Вычисление координат для размещения QR-кода на фоне по центру
        qr_x = (bg_width - self.qr_image.size[0]) // 2
        qr_y = (bg_height - self.qr_image.size[1]) // 2
        background.paste(self.qr_image, (qr_x, qr_y), self.qr_image)

        return background
