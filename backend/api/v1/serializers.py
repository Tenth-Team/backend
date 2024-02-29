from rest_framework import serializers

from ambassadors.models import (Ambassador, AmbassadorGoal, Content,
                                TrainingProgram)

from .utils import format_telegram_username
from ambassadors.choices import CONTENT_STATUS_CHOICES


class TrainingProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingProgram
        fields = ('id', 'name')


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class ContentSerializer(serializers.ModelSerializer):
    status = ChoiceField(choices=CONTENT_STATUS_CHOICES, required=False)

    class Meta:
        model = Content
        fields = '__all__'

    def create(self, validated_data):
        ambassador = Ambassador.objects.filter(
            telegram=validated_data['telegram']
        ).first()
        if ambassador:
            validated_data['ambassador'] = ambassador
            validated_data['full_name'] = ambassador.full_name
        content = Content.objects.create(**validated_data)
        return content

    def to_internal_value(self, instance):
        guide = instance.get('guide')
        if guide is not None:
            if not guide:
                instance['guide'] = 0
            else:
                instance['guide'] = 1
        instance = super().to_internal_value(instance)
        return instance

    def validate_telegram(self, value):
        return format_telegram_username(value)


class AmbassadorSerializer(serializers.ModelSerializer):
    ya_edu = serializers.CharField()
    amb_goal = serializers.CharField()

    class Meta:
        model = Ambassador
        fields = '__all__'

    def create(self, validated_data):
        ya_edu = validated_data.pop('ya_edu')
        goals = validated_data.pop('amb_goal')
        ambassador = Ambassador.objects.create(ya_edu=ya_edu, **validated_data)
        ambassador.amb_goal.add(*goals)
        return ambassador

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ya_edu'] = instance.ya_edu.name
        representation['amb_goal'] = [goal.name for goal in
                                      instance.amb_goal.all()]
        return representation

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        ya_edu_name = data.get('ya_edu')
        amb_goals = data.get('amb_goal')
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
        internal_value['amb_goal'] = goals
        return internal_value
