from django.db import models

from .choices import (
    CLOTHING_SIZES_CHOICES,
    CONTENT_STATUS_CHOICES,
    GENDER_CHOICES,
    MERCH_CHOICES,
    PROMO_CODE_STATUS_CHOICES,
    STATUS_CHOICES,
    STATUS_SEND_CHOICES,
)


class TrainingProgram(models.Model):
    """
    Модель названий программ обучения Яндекса.
    """

    name = models.CharField(max_length=255, verbose_name='Название программы')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Программа обучения'
        verbose_name_plural = 'Программы обучения'


class AmbassadorGoal(models.Model):
    """
    Модель названий целей амбассадорства.
    """

    name = models.CharField(max_length=255, verbose_name='Название цели')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цель амбассадорства'
        verbose_name_plural = 'Цели амбассадорства'


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
        null=True,
        verbose_name='Программа обучения',
    )
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=255, verbose_name='Адрес проживания')
    postal_code = models.CharField(max_length=20, verbose_name='Индекс')
    email = models.CharField(max_length=255, verbose_name='Адрес проживания')
    phone_number = models.CharField(
        max_length=20, verbose_name='Номер телефона'
    )
    telegram = models.CharField(max_length=100, verbose_name='Ник в телеграме')
    edu = models.TextField(max_length=1000, verbose_name='Образование')
    work = models.TextField(max_length=1000, verbose_name='Место работы')
    study_goal = models.TextField(
        max_length=1000, verbose_name='Цель обучения'
    )
    amb_goals = models.ManyToManyField(
        AmbassadorGoal,
        related_name='ambassadors',
        verbose_name='Цель амбассадорства',
    )
    blog_url = models.CharField(
        max_length=255, verbose_name='Ссылка на блоги', blank=True, null=True
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
        auto_now_add=True, verbose_name='Дата регистрации'
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Амбассадор'
        verbose_name_plural = 'Амбассадоры'


class PromoCode(models.Model):
    ambassador = models.ForeignKey(
        Ambassador,
        on_delete=models.CASCADE,
        related_name='promo_code',
        verbose_name='Амбассадор',
    )
    name = models.CharField(
        max_length=255, unique=True, verbose_name='Промокод'
    )
    status = models.CharField(
        max_length=10,
        choices=PROMO_CODE_STATUS_CHOICES,
        verbose_name='Статус промокода',
        default='active',
    )

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return self.name


class Content(models.Model):
    """
    Модель контента.
    """

    full_name = models.CharField(max_length=255, verbose_name='Имя и Фамилия')
    telegram = models.CharField(max_length=100, verbose_name='Ник в телеграме')
    link = models.CharField(max_length=200, verbose_name='Ссылка на контент')
    guide = models.BooleanField(verbose_name='В рамках Гайда?')
    status = models.CharField(
        max_length=50,
        default='new',
        choices=CONTENT_STATUS_CHOICES,
        verbose_name='Статус контента',
    )
    ambassador = models.ForeignKey(
        Ambassador,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='content',
    )
    created_date = models.DateField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Контент'
        verbose_name_plural = 'Контент'


class Merchandise(models.Model):
    """
    Модель мерча.
    """

    name = models.CharField(
        max_length=25, choices=MERCH_CHOICES, verbose_name='Название мерча'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Стоимость мерча',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мерч'
        verbose_name_plural = 'Мерч'


class MerchandiseShippingRequest(models.Model):
    """
    Модель заявки на отправку мерча.
    """

    name_merch = models.OneToOneField(
        Merchandise,
        on_delete=models.CASCADE,
        verbose_name='Название мерча',
    )
    ambassador = models.ForeignKey(
        Ambassador,
        on_delete=models.CASCADE,
        verbose_name='Амбассадор',
        related_name='merch_shipping_requests',
    )
    status_send = models.CharField(
        max_length=25,
        default='new',
        choices=STATUS_SEND_CHOICES,
        verbose_name='Статус отправки',
    )
    created_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    comment = models.TextField(
        max_length=200, verbose_name='Комментарий менеджера'
    )

    def __str__(self):
        return f'{self.name_merch} - {self.ambassador}'

    class Meta:
        verbose_name = 'Заявка на отправку мерча'
        verbose_name_plural = 'Заявки на отправку мерча'
