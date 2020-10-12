from rest_framework import serializers
from .models import Answers, Questions, QuestionOptions, Specialization
from rest_framework_nested.relations import NestedHyperlinkedRelatedField


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ('added', 'user_id', 'user_type', 'specialization',
                  'answers', 'userID', 'userFirstName', 'userLastName',
                  'userUserName')


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.StringRelatedField(many=True)
    # options = NestedHyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,   # Or add a queryset
    #     view_name='questions-options',
    #     parent_lookup_kwargs={'question_pk': 'question__pk'}
    # )

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
        model = Specialization
        fields = ('name',)
