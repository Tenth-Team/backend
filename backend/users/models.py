from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Модифицированная модель пользователя."""

    patronymic = models.CharField(max_length=150, verbose_name="Отчество")
    phone_regex = RegexValidator(
        regex=r"^\+\d{8,15}$",
        message="Номер телефона необходимо вводить в формате: "
        "«+999999999». Допускается до 15 цифр.",
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=16, unique=True
    )

    AbstractUser.REQUIRED_FIELDS += (
        "patronymic",
        "phone_number",
        "first_name",
        "last_name",
    )
