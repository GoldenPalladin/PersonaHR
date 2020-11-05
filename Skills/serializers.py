from rest_framework.serializers import ModelSerializer
from .models import Response, Skill


class SkillSerialiser(ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class SkillsSerialiser(ModelSerializer):
    skill = SkillSerialiser(many=False, required=False)

    class Meta:
        model = Response
        fields = '__all__'
