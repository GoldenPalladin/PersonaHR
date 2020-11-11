from rest_framework import serializers
#from .models import Match

class MatchSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256)
    