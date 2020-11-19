from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from Jobs.serializers import PositionSerializer, CVSerializer
from specializations.serializers import SkillSerialiser
from answers.models import Response
from .models import Respondent
from users.serializers import UserProfileSerializer, UserProfile


class AnswerSerializer(serializers.ModelSerializer):
    userProfile = UserProfileSerializer()

    class Meta:
        model = Respondent
        fields = ('added', 'user_id',  'specialization',
                  'answers', 'userProfile')

    def create(self, validated_data):
        user_profile_data = validated_data.pop('userProfile')
        profile_id = UserProfile.objects.create(**user_profile_data)
        return Respondent.objects.create(userProfile=profile_id, **validated_data)


class SkillResponsesSerialiser(ModelSerializer):
    skill = SkillSerialiser(many=False, required=False)
    position = PositionSerializer(many=False, required=False)
    cv = CVSerializer(many=False, required=False)

    class Meta:
        model = Response
        fields = '__all__'