from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .serializers import Questions, QuestionOptions, \
    QuestionDetailSerializer, QuestionListSerializer, \
    QuestionOptionSerializer, Specialization, SpecializationSerializer


class QuestionsViewSet(viewsets.ModelViewSet):
    """
    create:
    Options can be created via **post** from nested json element \n
    \t"options": \n
    \t\t[\n
    \t\t\t"order_no": int, \n
    \t\t\t"textForEmployer: str,\n
    \t\t\t"textForCandidate": str,\n
    \t\t\t"weight": int\n
    \t\t]
    """
    queryset = Questions.objects.all()
    serializer_class = QuestionListSerializer
    detail_serializer_class = QuestionDetailSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['specialization']

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


class QuestionOptionsViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionOptionSerializer

    def get_queryset(self):
        return QuestionOptions.objects.filter(question=self.kwargs[
            'question_pk'])


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
