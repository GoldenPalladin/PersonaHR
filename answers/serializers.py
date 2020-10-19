from rest_framework import serializers
from .models import Answers
from users.serializers import UserProfileSerializer, UserProfile


class AnswerSerializer(serializers.ModelSerializer):
    userProfile = UserProfileSerializer()

    class Meta:
        model = Answers
        fields = ('added', 'user_id',  'specialization',
                  'answers', 'userProfile')

    def create(self, validated_data):
        user_profile_data = validated_data.pop('userProfile')
        profile_id = UserProfile.objects.create(**user_profile_data)
        return Answers.objects.create(userProfile=profile_id, **validated_data)

