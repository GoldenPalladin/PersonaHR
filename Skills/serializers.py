from rest_framework.serializers import ModelSerializer
from .models import Response, Skill, SkillGroup
from Jobs.serializers import PositionSerializer, CVSerializer


class SkillGroupSerialiser(ModelSerializer):
    class Meta:
        model = SkillGroup
        fields = '__all__'


class SkillSerialiser(ModelSerializer):
    group = SkillGroupSerialiser(many=False, required=False)

    class Meta:
        model = Skill
        fields = '__all__'


class SkillResponsesSerialiser(ModelSerializer):
    skill = SkillSerialiser(many=False, required=False)
    position = PositionSerializer(many=False, required=False)
    cv = CVSerializer(many=False, required=False)

    class Meta:
        model = Response
        fields = '__all__'
