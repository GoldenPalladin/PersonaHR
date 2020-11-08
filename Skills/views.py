from django.utils.decorators import method_decorator
from rest_framework import viewsets
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING, TYPE_INTEGER
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import Skill, Response, SkillSerialiser, \
    SkillGroup, SkillGroupSerialiser, SkillResponsesSerialiser


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


param_skill = Parameter('skillId',
                       in_=IN_QUERY,
                       description='Skill id to filter responses',
                       type=TYPE_INTEGER)

param_position = Parameter('positionId',
                           in_=IN_QUERY,
                           description='Position id to filter responses',
                           type=TYPE_INTEGER)

param_cv = Parameter('cvId',
                     in_=IN_QUERY,
                     description='CV id to filter responses',
                     type=TYPE_INTEGER)


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      manual_parameters=[param_skill, param_position, param_cv],
                      operation_id='Get skill responses list',
                      operation_description='Get list of skill responses',
                      tags=['Skills']
                  ))
@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(
                      operation_id='Get skill response details',
                      operation_description='Get skill group by id',
                      tags=['Skills']
                  ))
@method_decorator(name='create',
                  decorator=swagger_auto_schema(
                      operation_id='Create new skill response',
                      operation_description='Create new skill response',
                      tags=['Skills']
                  ))
@method_decorator(name='update',
                  decorator=swagger_auto_schema(
                      operation_id='Update skill response',
                      operation_description='Update skill response details',
                      tags=['Skills']
                  ))
class SkillResponsesViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = SkillResponsesSerialiser
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['skill']
    http_method_names = ['get', 'post', 'put', 'head']

    def get_queryset(self):
        queryset = Response.objects.all()
        skill_id = self.request.query_params.get('skillId', None)
        position_id = self.request.query_params.get('positionId', None)
        cv_id = self.request.query_params.get('cvId', None)
        if skill_id is not None:
            queryset = queryset.filter(skill=skill_id)
        if position_id is not None:
            queryset = queryset.filter(position=position_id)
        if cv_id is not None:
            queryset = queryset.filter(cv=cv_id)
        return queryset
