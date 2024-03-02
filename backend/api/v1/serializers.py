from rest_framework import serializers

from ambassadors.models import (
    Ambassador,
    AmbassadorGoal,
    Content,
    TrainingProgram,
)

from .utlis import format_telegram_username


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


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


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
        representation['amb_goals'] = [goal.name for goal in
                                       instance.amb_goals.all()]
        return representation

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        ya_edu_name = data.get('ya_edu')
        amb_goals = data.get('amb_goals')
        telegram = data.get('telegram')

        goals = []
        for goal in amb_goals.split(', '):
            goal, created = AmbassadorGoal.objects.get_or_create(
                name=goal
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

    class Meta:
        model = Ambassador
        fields = '__all__'
