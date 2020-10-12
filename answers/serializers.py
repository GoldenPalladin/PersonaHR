from rest_framework import serializers
from .models import Answers, Questions, QuestionOptions, Specialization


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ('added', 'user_id', 'user_type', 'specialization',
                  'answer_data')


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.StringRelatedField(many=True)

    class Meta:
        model = Questions
        fields = ('specialization', 'question_type', 'em_text', 'ca_text',
                  'weight', 'options')


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOptions
        fields = ('question', 'order_no', 'em_text', 'ca_text', 'weight')


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOptions
        fields = ('name',)
