from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_INTEGER
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from answers.models import Response
from answers.serializers import SkillResponsesSerialiser

from .models import Respondent
from .serializers import RespondentSerializer


class RespondentViewSet(viewsets.ModelViewSet):
    queryset = Respondent.objects.all()
    serializer_class = RespondentSerializer


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