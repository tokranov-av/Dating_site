import os
from PIL import Image, ImageEnhance
from django.core.exceptions import ValidationError
from dating_site import settings


class Watermark:
    """Класс наложения водяного знака в загруженное изображение."""
    def process(self, image):
        watermark_path = os.path.join(
            settings.STATIC_ROOT, 'watermark/watermark.png'
        )
        watermark = Image.open(watermark_path).convert('RGBA')
        width, height = image.size
        watermark.thumbnail((width // 7, height // 7), Image.ANTIALIAS)
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(1)
        watermark.putalpha(alpha)
        layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        layer.paste(watermark, (0, 0))
        return Image.composite(layer, image, layer)


def get_default_avatar():
    """Функция возврата пути расположения изображения профиля по умолчанию."""
    return "default_avatar/default_avatar.jpg"


def validate_size_image(file_obj):
    """Функция проверки размера файла."""
    megabyte_limit = 2
    if file_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(
            f'{"Максимальный размер файла"} {megabyte_limit} MB'
        )


def validator_latitude(value):
    """Проверка правильности ввода широты."""
    if not (-90 <= value <= 90):
        raise ValidationError(
            'Координаты должны входит в диапазон от минус 90 до 90 градусов.'
        )


def validator_longitude(value):
    """Проверка правильности ввода долготы."""
    if not (-180 <= value <= 180):
        raise ValidationError(
            'Координаты должны входит в диапазон от минус 180 до 180 градусов.'
        )
