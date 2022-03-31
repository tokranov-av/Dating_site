from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from imagekit.models import ProcessedImageField
from .managers import MyUserManager
from .services import (
    Watermark, validator_latitude, validator_longitude, get_default_avatar,
    validate_size_image
)


class User(AbstractUser):
    """Модель пользователя."""
    GENDER = (
        ('male', 'Мужской'),
        ('female', 'Женский'),
    )

    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=150)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150)
    gender = models.CharField(
        max_length=12, choices=GENDER, verbose_name='Пол'
    )
    latitude = models.DecimalField(
        max_digits=18, decimal_places=16, verbose_name='Широта (в градусах)',
        default=None, null=True, validators=[validator_latitude]
    )
    longitude = models.DecimalField(
        max_digits=19, decimal_places=16, verbose_name='Долгота (в градусах)',
        default=None, null=True, validators=[validator_longitude]
    )
    avatar = ProcessedImageField(
        upload_to='user_avatars/', processors=[Watermark()], format='JPEG',
        options={'quality': 72}, verbose_name='Аватар',
        default=get_default_avatar,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg']),
            validate_size_image
        ]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']


class LikedUsers(models.Model):
    """Модель хранения понравившихся пользователей."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user',
        verbose_name='Пользователь'
    )
    liked_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='liked_user',
        verbose_name='Понравившийся пользователь'
    )
    send_email = models.BooleanField(
        default=False, verbose_name='Обмен email'
    )

    class Meta:
        verbose_name = 'Понравившийся пользователь'
        verbose_name_plural = 'Понравившийся пользователи'
        ordering = ['id']
