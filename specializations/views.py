from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING, TYPE_INTEGER
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from lib.swagged_view import SwaggedViewSet, add_swagger
from specializations.models import SkillGroup, Skill
from specializations.serializers import SkillGroupSerialiser, SkillSerialiser

from .serializers import Questions, QuestionOptions, \
    QuestionDetailSerializer, QuestionListSerializer, \
    QuestionOptionSerializer, Specialization, SpecializationSerializer

param_specialization = Parameter('specializationId',
                                 in_=IN_QUERY,
                                 description='Specialization id to filter '
                                             'the quiestions',
                                 type=TYPE_INTEGER)
param_question_type = Parameter('type',
                                in_=IN_QUERY,
                                description='Return the questions of '
                                            'specified type',
                                type=TYPE_STRING)
param_name = Parameter('name',
                       in_=IN_QUERY,
                       description='Specialization name for '
                                   '\'contains\' search',
                       type=TYPE_STRING)


question_swagger_details = [
    ('list', 'Get list of question', 'Get list of questions with filter '
                                    'options',
     ['Questions'], [param_specialization,
                     param_question_type]),
    ('retrieve', 'Get question details', 'Get question by id',
     ['Questions'], []),
    ('create', 'Create new question', 'Create new question with options',
     ['Questions'], []),
    ('update', 'Update question', 'Update question with specified id',
     ['Questions'], [])
]
@add_swagger(question_swagger_details)
class QuestionsViewSet(SwaggedViewSet):
    queryset = Questions.objects.all()
    serializer_class = QuestionListSerializer
    detail_serializer_class = QuestionDetailSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['specialization']
    params = ['specializationId', 'type']


options_swagger_details = [
    ('list', 'Get question options', 'Get list of options for the question',
     ['Questions'], [param_specialization,
                     param_question_type]),
    ('retrieve', 'Get option details', 'Get option by id',
     ['Questions'], []),
    ('create', 'Create new option', 'Create new option for the question',
     ['Questions'], []),
    ('update', 'Update option', 'Update option details',
     ['Questions'], [])
]
@add_swagger(options_swagger_details)
class QuestionOptionsViewSet(SwaggedViewSet):

    serializer_class = QuestionOptionSerializer
    http_method_names = ['get', 'post', 'put', 'head']

    def get_queryset(self):
        return QuestionOptions.objects.filter(question=self.kwargs[
            'question_pk'])


specialization_swagger_details = [
    ('list', 'Get specializations', 'Get list specializations',
     ['Questions'], [param_name, ]),
    ('retrieve', 'Get specialization details', 'Get specialization by id',
     ['Questions'], []),
    ('create', 'Create new specialization', 'Create new specialization',
     ['Questions'], []),
    ('update', 'Update specialization', 'Update specialization details',
     ['Questions'], [])
]
@add_swagger(specialization_swagger_details)
class SpecializationViewSet(SwaggedViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    params = ['name', ]


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      operation_id='Get groups list',
                      operation_description='Get list of skill groups',
                      tags=['Skills']
                  ))
@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(
                      operation_id='Get group details',
                      operation_description='Get skill group by id',
                      tags=['Skills']
                  ))
@method_decorator(name='create',
                  decorator=swagger_auto_schema(
                      operation_id='Create new group',
                      operation_description='Create new skill group',
                      tags=['Skills']
                  ))
@method_decorator(name='update',
                  decorator=swagger_auto_schema(
                      operation_id='Update group',
                      operation_description='Update skill group details',
                      tags=['Skills']
                  ))
class SkillGroupViewSet(viewsets.ModelViewSet):
    queryset = SkillGroup.objects.all()
    serializer_class = SkillGroupSerialiser
    http_method_names = ['get', 'post', 'put', 'head']


param_skill_group = Parameter('skillGroup',
                              in_=IN_QUERY,
                              description='Group id to filter the skills',
                              type=TYPE_INTEGER)


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      manual_parameters=[param_skill_group, ],
                      operation_id='Get skills list',
                      operation_description='Get list of skills with filter '
                                            'options',
                      tags=['Skills']
                  ))
@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(
                      operation_id='Get skill details',
                      operation_description='Get skill by id',
                      tags=['Skills']
                  ))
@method_decorator(name='create',
                  decorator=swagger_auto_schema(
                      operation_id='Create new skill',
                      operation_description='Create new skill',
                      tags=['Skills']
                  ))
@method_decorator(name='update',
                  decorator=swagger_auto_schema(
                      operation_id='Update skill',
                      operation_description='Update skill details',
                      tags=['Skills']
                  ))
class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerialiser
    http_method_names = ['get', 'post', 'put', 'head']

    def get_queryset(self):
        queryset = Skill.objects.all()
        skill_group = self.request.query_params.get('skillGroup', None)
        if skill_group is not None:
            queryset = queryset.filter(skillGroup=skill_group)
        return queryset