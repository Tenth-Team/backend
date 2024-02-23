from django.db import models
from choices import GENDER_CHOICES, STATUS_CHOICES, CLOTHING_SIZES_CHOICES


class TrainingProgram(models.Model):
    """
    Модель названий программ обучения Яндекса.
    """

    name = models.CharField(max_length=255, verbose_name='Название программы')


class AmbassadorGoal(models.Model):
    """
    Модель названий целей амбассадорства.
    """

    name = models.CharField(max_length=255, verbose_name='Название цели')


class Ambassador(models.Model):
    """
    Модель амбассадора.
    """

    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name='Пол',
    )
    ya_edu = models.ForeignKey(
        TrainingProgram,
        on_delete=models.SET_NULL,
        verbose_name='Программа обучения',
    )
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=255, verbose_name='Адрес проживания')
    postal_code = models.CharField(max_length=20, verbose_name='Индекс')
    email = models.CharField(max_length=255, verbose_name='Адрес проживания')
    phone_number = models.CharField(
        max_length=20,
        verbose_name='Номер телефона'
    )
    telegram = models.CharField(max_length=100, verbose_name='Ник в телеграме')
    edu = models.TextField(max_length=1000, verbose_name='Образование')
    work = models.TextField(max_length=1000, verbose_name='Место работы')
    study_goal = models.TextField(
        max_length=1000, verbose_name='Цель обучения'
    )
    amb_goal = models.ManyToManyField(
        AmbassadorGoal,
        related_name='ambassadors',
        verbose_name='Цель амбассадорства',
    )
    blog_url = models.CharField(
        max_length=255,
        verbose_name='Ссылка на блоги',
        blank=True,
        null=True
    )
    clothing_size = models.CharField(
        max_length=3,
        choices=CLOTHING_SIZES_CHOICES,
        verbose_name='Размер одежды',
    )
    shoe_size = models.CharField(max_length=50, verbose_name='Размер обуви')
    additional_comments = models.TextField(
        max_length=2000,
        verbose_name='Дополнительная информация',
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=50,
        default='pending',
        choices=STATUS_CHOICES,
        verbose_name='Статус амбассадора',
    )
    reg_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации'
    )
