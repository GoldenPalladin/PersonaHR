from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING, TYPE_INTEGER
from drf_yasg.utils import swagger_auto_schema

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


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      manual_parameters=[param_specialization,
                                         param_question_type],
                      operation_id='Get list of questions',
                      operation_description='Get list of questions with filter '
                                            'options',
                      tags=['Questions']
                  ))
@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(
                      operation_id='Get question details',
                      operation_description='Get question by id',
                      tags=['Questions']
                  ))
@method_decorator(name='create',
                  decorator=swagger_auto_schema(
                      operation_id='Create new question',
                      operation_description='Create new question with options',
                      tags=['Questions']
                  ))
@method_decorator(name='update',
                  decorator=swagger_auto_schema(
                      operation_id='Update question',
                      operation_description='Update question with specified id',
                      tags=['Questions']
                  ))
class QuestionsViewSet(viewsets.ModelViewSet):
    queryset = Questions.objects.all()
    serializer_class = QuestionListSerializer
    detail_serializer_class = QuestionDetailSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['specialization']
    http_method_names = ['get', 'post', 'put', 'head']

    def get_serializer_class(self):
        """
        Determine which serializer to user `list` or `detail`
        """
        if self.action == 'retrieve':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class

        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        kwargs.update({'partial': True})
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Questions.objects.all()
        specialization = self.request.query_params.get('specializationId', None)
        question_type = self.request.query_params.get('type', None)
        if specialization is not None:
            queryset = queryset.filter(specialization=specialization)
        if question_type is not None:
            queryset = queryset.filter(questionType=question_type)
        return queryset


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      manual_parameters=[param_specialization,
                                         param_question_type],
                      operation_id='Get question options',
                      operation_description='Get list of options for the '
                                            'question',
                      tags=['Questions']
                  ))
@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(
                      operation_id='Get option',
                      operation_description='Get option by id',
                      tags=['Questions']
                  ))
@method_decorator(name='create',
                  decorator=swagger_auto_schema(
                      operation_id='Create new option',
                      operation_description='Create new option for the '
                                            'question',
                      tags=['Questions']
                  ))
@method_decorator(name='update',
                  decorator=swagger_auto_schema(
                      operation_id='Update option',
                      operation_description='Update option details',
                      tags=['Questions']
                  ))
class QuestionOptionsViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionOptionSerializer
    http_method_names = ['get', 'post', 'put', 'head']

    def get_queryset(self):
        return QuestionOptions.objects.filter(question=self.kwargs[
            'question_pk'])


param_name = Parameter('name',
                       in_=IN_QUERY,
                       description='Specialization name for '
                                   '\'contains\' search',
                       type=TYPE_STRING)


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      manual_parameters=[param_name],
                      operation_id='Get list of specializations',
                      operation_description='Get list of specializations '
                                            'with filter options',
                      tags=['Specializations']
                  ))
@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(
                      operation_id='Get specialization details',
                      operation_description='Get specialization by id',
                      tags=['Specializations']
                  ))
@method_decorator(name='create',
                  decorator=swagger_auto_schema(
                      operation_id='Create new specialization',
                      operation_description='Create new specialization',
                      tags=['Specializations']
                  ))
@method_decorator(name='update',
                  decorator=swagger_auto_schema(
                      operation_id='Update specialization',
                      operation_description='Update specialization with '
                                            'specified id',
                      tags=['Specializations']
                  ))
class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self):
        queryset = Specialization.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__contains=name)

        return queryset
