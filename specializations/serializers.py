from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from specializations.models import SkillGroup, Skill
from .models import Questions, QuestionOptions, Specialization


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOptions
        fields = '__all__'

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
        fields = ('id', 'specialization', 'textForEmployer',
                  'textForCandidate', 'options')

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
        fields = ('id', 'specialization', 'textForEmployer',
                  'textForCandidate', 'options')

    def update(self, instance, validated_data):
        instance.question_type = validated_data.get('questionType',
                                                    instance.question_type)
        instance.em_text = validated_data.get('textForEmployer',
                                              instance.em_text)
        instance.ca_text = validated_data.get('textForCandidate',
                                              instance.ca_text)
        instance.save()


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ('name',)


class SkillGroupSerialiser(ModelSerializer):
    class Meta:
        model = SkillGroup
        fields = '__all__'


class SkillSerialiser(ModelSerializer):
    group = SkillGroupSerialiser(many=False, required=False)

    class Meta:
        model = Skill
        fields = '__all__'