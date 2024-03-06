import re

from rest_framework import serializers

from ambassadors.models import (
    Ambassador,
    AmbassadorGoal,
    Content,
    MerchandiseShippingRequest,
    PromoCode,
    TrainingProgram,
)

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


class ContentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Контента.
    """

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
        обрабатывает логическое поле 'guide'.
        """
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

    class Meta:
        model = Ambassador
        fields = '__all__'

    def create(self, validated_data):
        ya_edu = validated_data.pop('ya_edu')
        goals = validated_data.pop('amb_goals')
        ambassador = Ambassador.objects.create(ya_edu=ya_edu, **validated_data)
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

        goals = []
        for goal in re.split(r', (?=[А-Я])', amb_goals):
            goal, created = AmbassadorGoal.objects.get_or_create(
                name=goal.strip()
            )
            goals.append(goal)

        training_program, created = TrainingProgram.objects.get_or_create(
            name=ya_edu_name
        )

        internal_value['ya_edu'] = training_program
        internal_value['amb_goals'] = goals
        internal_value['telegram'] = format_telegram_username(telegram)
        return internal_value


class AmbassadorCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания амбассадоров.
    """

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

    class Meta:
        model = Ambassador
        fields = '__all__'

    def get_promo_code(self, obj):
        promo_code = obj.promo_code.first()
        if promo_code is not None:
            return promo_code.name
        return None


class MerchandiseShippingRequestSerializer(serializers.ModelSerializer):
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
        return MerchandiseShippingRequestSerializer(
            shipped_merch, many=True
        ).data
