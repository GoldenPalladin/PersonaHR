from rest_framework import serializers
from .models import Position, CV


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = '__all__'
