from rest_framework import serializers
from .models import Answers, Questions, QuestionOptions, \
    Specialization, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('userType', 'leadSource', 'userID', 'userFirstName',
                  'userLastName', 'userUserName')


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


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOptions
        fields = ('id', 'question', 'order_no', 'textForEmployer',
                  'textForCandidate', 'weight')

    def __init__(self, *args, **kwargs):
        """
        if Options are created with nested json 'question' relation will be
        created in 'create' method in QuestionListSerializer
        :param args:
        :param kwargs:
        """
        create_options = kwargs.pop('create_options', False)
        super(QuestionOptionSerializer, self).__init__(*args, **kwargs)
        if create_options:
            self.fields.pop('question')


class QuestionListSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, required=False,
                                       create_options=True)

    class Meta:
        model = Questions
        fields = ('id', 'specialization', 'questionType', 'textForEmployer',
                  'textForCandidate', 'weight', 'options')

    def create(self, validated_data):
        options_data = validated_data.pop('options', None)
        question = Questions.objects.create(**validated_data)
        if options_data:
            for option_data in options_data:
                QuestionOptions.objects.create(question=question, **option_data)
        return question


class QuestionDetailSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, required=False)

    class Meta:
        model = Questions
        fields = ('id', 'specialization', 'questionType', 'textForEmployer',
                  'textForCandidate', 'weight', 'options')

    def update(self, instance, validated_data):
        instance.question_type = validated_data.get('questionType',
                                                    instance.question_type)
        instance.em_text = validated_data.get('textForEmployer',
                                              instance.em_text)
        instance.ca_text = validated_data.get('textForCandidate',
                                              instance.ca_text)
        instance.weight = validated_data.get('weight',
                                             instance.weight)
        instance.save()


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ('name',)
