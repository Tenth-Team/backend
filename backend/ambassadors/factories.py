import factory
from factory import Faker
from factory.django import DjangoModelFactory

from .choices import CLOTHING_SIZES_CHOICES, GENDER_CHOICES, STATUS_CHOICES
from .models import Ambassador, AmbassadorGoal, City, Country, TrainingProgram


class CityFactory(DjangoModelFactory):
    class Meta:
        model = City

    name = Faker('city')


class CountryFactory(DjangoModelFactory):
    class Meta:
        model = Country

    name = Faker('country')


class TrainingProgramFactory(DjangoModelFactory):
    class Meta:
        model = TrainingProgram

    name = Faker('sentence', nb_words=4)


class AmbassadorGoalFactory(DjangoModelFactory):
    class Meta:
        model = AmbassadorGoal

    name = Faker('sentence', nb_words=6)


class AmbassadorFactory(DjangoModelFactory):
    class Meta:
        model = Ambassador

    full_name = Faker('name')
    gender = Faker('random_element',
                   elements=[choice[0] for choice in GENDER_CHOICES])
    ya_edu = factory.SubFactory(TrainingProgramFactory)
    country = factory.SubFactory(CountryFactory)
    city = factory.SubFactory(CityFactory)
    address = Faker('street_address')
    postal_code = Faker('postcode')
    email = Faker('email')
    phone_number = Faker('phone_number')
    telegram = Faker('user_name')
    edu = Faker('text', max_nb_chars=200)
    work = Faker('company')
    study_goal = Faker('text', max_nb_chars=200)
    blog_url = Faker('url')
    clothing_size = Faker('random_element', elements=[choice[0] for choice in
                                                      CLOTHING_SIZES_CHOICES])
    shoe_size = Faker('random_element',
                      elements=['38', '39', '40', '41', '42', '43', '44',
                                '45'])
    additional_comments = Faker('text', max_nb_chars=200)
    status = Faker('random_element',
                   elements=[choice[0] for choice in STATUS_CHOICES])
