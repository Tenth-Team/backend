import factory
from factory import Faker
from factory.django import DjangoModelFactory

from .choices import (
    CLOTHING_SIZES_CHOICES,
    CONTENT_STATUS_CHOICES,
    GENDER_CHOICES,
    MERCH_CHOICES,
    PROMO_CODE_STATUS_CHOICES,
    STATUS_CHOICES,
    STATUS_SEND_CHOICES,
)
from .models import (
    Ambassador,
    AmbassadorGoal,
    City,
    Content,
    Country,
    Merchandise,
    MerchandiseShippingRequest,
    PromoCode,
    TrainingProgram,
)


class CityFactory(DjangoModelFactory):
    """
    Фабрика для модели городов.
    """
    class Meta:
        model = City

    name = Faker('city')


class CountryFactory(DjangoModelFactory):
    """
    Фабрика для модели стран.
    """
    class Meta:
        model = Country

    name = Faker('country')


class TrainingProgramFactory(DjangoModelFactory):
    """
    Фабрика для модели программ обучения.
    """
    class Meta:
        model = TrainingProgram

    name = Faker('sentence', nb_words=4)


class AmbassadorGoalFactory(DjangoModelFactory):
    """
    Фабрика для модели целей амбассадорства.
    """
    class Meta:
        model = AmbassadorGoal

    name = Faker('sentence', nb_words=6)


class AmbassadorFactory(DjangoModelFactory):
    """
    Фабрика для модели амбассадора.
    """
    class Meta:
        model = Ambassador

    full_name = Faker('name')
    gender = Faker(
        'random_element', elements=[choice[0] for choice in GENDER_CHOICES]
    )
    ya_edu = factory.SubFactory(TrainingProgramFactory)
    country = factory.SubFactory(CountryFactory)
    city = factory.SubFactory(CityFactory)
    address = str(Faker('street_address'))[:20]
    postal_code = Faker('postcode')
    email = Faker('email')
    phone_number = str(Faker('phone_number'))[:20]
    telegram = Faker('user_name')
    edu = Faker('text', max_nb_chars=200)
    work = Faker('company')
    study_goal = Faker('text', max_nb_chars=200)
    blog_url = Faker('url')
    clothing_size = Faker(
        'random_element',
        elements=[choice[0] for choice in CLOTHING_SIZES_CHOICES],
    )
    shoe_size = Faker(
        'random_element',
        elements=['38', '39', '40', '41', '42', '43', '44', '45'],
    )
    additional_comments = Faker('text', max_nb_chars=200)
    status = Faker(
        'random_element', elements=[choice[0] for choice in STATUS_CHOICES]
    )


class ContentFactory(DjangoModelFactory):
    """
    Фабрика для модели контента.
    """
    class Meta:
        model = Content

    full_name = Faker('name')
    telegram = Faker('user_name')
    link = Faker('url')
    guide = Faker('random_element', elements=[True, False])
    status = Faker(
        'random_element',
        elements=[choice[0] for choice in CONTENT_STATUS_CHOICES],
    )
    ambassador = factory.SubFactory(AmbassadorFactory)
    comment = Faker('text', max_nb_chars=200)


class PromoCodeFactory(DjangoModelFactory):
    """
    Фабрика для модели промокодов.
    """
    class Meta:
        model = PromoCode

    ambassador = factory.SubFactory(AmbassadorFactory)
    name = Faker('lexify', text='?' * 16)
    status = Faker(
        'random_element',
        elements=[choice[0] for choice in PROMO_CODE_STATUS_CHOICES],
    )


class MerchandiseFactory(DjangoModelFactory):
    """
    Фабрика для модели мерча.
    """
    class Meta:
        model = Merchandise

    name = Faker(
        'random_element',
        elements=[choice[0] for choice in MERCH_CHOICES]
    )
    price = Faker(
        'random_element',
        elements=[100, 1000]
    )


class MerchandiseShippingRequestFactory(DjangoModelFactory):
    """
    Фабрика для модели заявок на мерч.
    """
    class Meta:
        model = MerchandiseShippingRequest

    name_merch = factory.SubFactory(MerchandiseFactory)
    ambassador = factory.SubFactory(AmbassadorFactory)
    status_send = Faker(
        'random_element',
        elements=[choice[0] for choice in STATUS_SEND_CHOICES]
    )
    comment = Faker('text')
