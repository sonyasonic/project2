from qr_code_generator import QRCodeGenerator, QRCodeWithBackground
from exceptions import InvalidURL, InvalidData


# Мы использовали информацию по этим ссылкам:
# https://realpython.com/python-generate-qr-code/
# https://pydocs.ru/python-qr-code/
# Также нами использовались нейросети (одна из ним: Марти GPT) для обнаружения ошибок в коде

def main():

    try:
    # Ввод данных для QR-кода
        user_data = input("Введите текст для QR-кода, который вы увидите после сканирования: ")

    # Ввод формы QR-кода
        valid_shapes = ['square', 'circle', 'rounded_square']
        while True:
            shape_choice = input("Выберите форму QR-кода (square, circle, rounded_square): ")
            if shape_choice in valid_shapes:
                break
            print("Ошибка: форма не распознана. Пожалуйста, выберите из доступных.")

    # Ввод цвета для QR-кода и его фона
        fill_color = QRCodeGenerator.get_color("Введите цвет заливки (пикселей) для QR-кода: ")
        bg_color = QRCodeGenerator.get_color("Введите цвет фона для QR-кода: ")

    # Генерация QR-кода
        qr_gen = QRCodeGenerator(user_data, shape_choice)
        qr_image = qr_gen.generate_qr_image(fill_color=fill_color, back_color=bg_color)

    # Ввод URL для фонового изображения
        while True:
            background_url = input("Введите URL для изображения фона: ")
            try:
                qr_with_bg = QRCodeWithBackground(qr_image, background_url)
                final_image = qr_with_bg.apply_background()
                break
            except InvalidURL as e:
                print(e) # Печатает ошибку, если URL недопустим

    # Сохранение финального изображения
        final_image.save("final_qrcode.png")
        print("QR-код с цветом и формой успешно сохранен как 'final_qrcode.png'.")

    except InvalidData as e:
        print(f"Ошибка в данных QR-кода: {e}")
    except InvalidURL as e:
        print(f"Ошибка с URL: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__=="__main__":
    main()