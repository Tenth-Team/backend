from ambassadors.models import Ambassador, Content
from rest_framework import serializers


class AmbassadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambassador
        fields = '__all__'


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'
