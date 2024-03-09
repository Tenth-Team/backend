import re

from ambassadors.choices import CONTENT_STATUS_CHOICES
from ambassadors.models import (
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
from rest_framework import serializers

from .utils import format_telegram_username


class TrainingProgramSerializer(serializers.ModelSerializer):
    """
    Сериализатор для программ обучения.
    """

    class Meta:
        model = TrainingProgram
        fields = ('id', 'name')


class AmbassadorGoalSerializer(serializers.ModelSerializer):
    """
    Сериализатор для целей амбассадорства.
    """

    class Meta:
        model = AmbassadorGoal
        fields = ('id', 'name')


class PromoCodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели промокода.
    """

    class Meta:
        model = PromoCode
        fields = '__all__'


class ShortPromoCodeSerializer(serializers.ModelSerializer):
    """
    Короткий сериализатор для модели промокода.
    """

    class Meta:
        model = PromoCode
        fields = ('name', 'status')


class ContentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Контента.
    """

    status = serializers.ChoiceField(
        choices=CONTENT_STATUS_CHOICES,
        required=False,
        help_text='Статус контента. Возможные значения: '
        'new, approved, rejected.',
    )

    class Meta:
        """
        Класс Meta указывает на модель и поля,
        которые будут использоваться сериализатором.
        """

        model = Content
        fields = '__all__'
        extra_kwargs = {
            'ambassador': {'required': False},
            'status': {'required': False},
        }

    def create(self, validated_data):
        """
        Создаёт новый экземпляр контента на основе проверенных данных.
        """
        ambassador = Ambassador.objects.filter(
            telegram=validated_data['telegram']
        ).first()
        if ambassador:
            validated_data['ambassador'] = ambassador
            validated_data['full_name'] = ambassador.full_name
        content = Content.objects.create(**validated_data)
        return content

    def to_internal_value(self, instance):
        """
        Преобразует данные перед сохранением,
        преобразовывает 'guide' в булевый тип.
        """

        instance = instance.copy()
        guide = instance.get('guide')
        if guide is not None:
            instance['guide'] = bool(guide)
        return super().to_internal_value(instance)

    def validate_telegram(self, value):
        """
        Проверяет и форматирует имя пользователя в Telegram перед сохранением.
        """
        return format_telegram_username(value)


class YandexFormAmbassadorCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания амбассадоров из Яндекс форм.
    """

    ya_edu = serializers.CharField()
    amb_goals = serializers.CharField()
    city = serializers.CharField()
    country = serializers.CharField()

    class Meta:
        model = Ambassador
        fields = '__all__'

    def create(self, validated_data):
        ya_edu = validated_data.pop('ya_edu')
        goals = validated_data.pop('amb_goals')
        country = validated_data.pop('country')
        city = validated_data.pop('city')
        ambassador = Ambassador.objects.create(
            ya_edu=ya_edu, country=country, city=city, **validated_data
        )
        ambassador.amb_goals.add(*goals)
        return ambassador

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ya_edu'] = instance.ya_edu.name
        representation['amb_goals'] = [
            goal.name for goal in instance.amb_goals.all()
        ]
        return representation

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        ya_edu_name = data.get('ya_edu')
        amb_goals = data.get('amb_goals')
        telegram = data.get('telegram')
        country = data.get('country')
        city = data.get('city')

        goals = []
        for goal in re.split(r', (?=[А-Я])', amb_goals):
            goal, created = AmbassadorGoal.objects.get_or_create(
                name=goal.strip()
            )
            goals.append(goal)

        training_program, created = TrainingProgram.objects.get_or_create(
            name=ya_edu_name
        )
        country, created = Country.objects.get_or_create(name=country)
        city, created = City.objects.get_or_create(name=city)
        internal_value['country'] = country
        internal_value['city'] = city
        internal_value['ya_edu'] = training_program
        internal_value['amb_goals'] = goals
        internal_value['telegram'] = format_telegram_username(telegram)
        return internal_value


class AmbassadorCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания амбассадоров.
    """

    city = serializers.CharField()
    country = serializers.CharField()

    def create(self, validated_data):
        amb_goals_data = validated_data.pop('amb_goals')
        country_data = validated_data.pop('country')
        city_data = validated_data.pop('city')

        ambassador = super().create(validated_data)

        country, _ = Country.objects.get_or_create(name=country_data)
        ambassador.country = country
        city, _ = City.objects.get_or_create(name=city_data)
        ambassador.city = city

        ambassador.save()
        ambassador.amb_goals.set(amb_goals_data)
        return ambassador

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        telegram = data.get('telegram')
        country = data.get('country')
        city = data.get('city')

        country, _ = Country.objects.get_or_create(name=country)
        city, _ = City.objects.get_or_create(name=city)
        internal_value['country'] = country
        internal_value['city'] = city
        internal_value['telegram'] = format_telegram_username(telegram)
        return internal_value

    class Meta:
        model = Ambassador
        fields = '__all__'


class AmbassadorUpdateSerializer(serializers.ModelSerializer):
    city = serializers.CharField(required=False)
    country = serializers.CharField(required=False)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        telegram = data.get('telegram')
        country = data.get('country')
        city = data.get('city')
        if country:
            country, _ = Country.objects.get_or_create(name=country)
            internal_value['country'] = country
        if city:
            city, _ = City.objects.get_or_create(name=city)
            internal_value['city'] = city
        if telegram:
            internal_value['telegram'] = format_telegram_username(telegram)
        return internal_value

    class Meta:
        model = Ambassador
        fields = '__all__'


class AmbassadorReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения амбассадоров.
    """

    ya_edu = TrainingProgramSerializer()
    amb_goals = AmbassadorGoalSerializer(many=True)
    promo_code = serializers.SerializerMethodField()
    content_count = serializers.SerializerMethodField()
    city = serializers.SlugRelatedField(read_only=True, slug_field='name')
    country = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Ambassador
        fields = '__all__'

    def get_promo_code(self, obj):
        promo_code = obj.prefetched_promo_codes
        if promo_code:
            return promo_code[0].name
        return None

    def get_content_count(self, obj):
        return obj.content.count()


class LoyaltyMerchandiseShippingRequestSerializer(serializers.ModelSerializer):
    """Сериализатор для представления заявки на отправку мерча."""

    name_merch = serializers.SlugRelatedField(
        read_only=True, slug_field='name'
    )

    class Meta:
        model = MerchandiseShippingRequest
        fields = '__all__'


class LoyaltyAmbassadorSerializer(serializers.ModelSerializer):
    """Сериализатор для получения данных
    амбассадора для страницы лояльности."""

    content_count = serializers.SerializerMethodField(read_only=True)
    shipped_merch = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ambassador
        fields = ('id', 'full_name', 'content_count', 'shipped_merch')

    def get_content_count(self, ambassador):
        """Возвращает количество одобренных публикаций амбассадора"""
        return len(ambassador.content_prefetch)

    def get_shipped_merch(self, ambassador):
        """Возвращает список заявок отправленного амбассадору мерча."""
        shipped_merch = ambassador.shipped_merch_prefetch
        return LoyaltyMerchandiseShippingRequestSerializer(
            shipped_merch, many=True
        ).data


class MerchandiseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для мерча.
    """

    class Meta:
        model = Merchandise
        fields = ('id', 'name')


class MerchandiseShippingRequestSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели заявки на отправку мерча.
    """

    class Meta:
        model = MerchandiseShippingRequest
        fields = '__all__'
