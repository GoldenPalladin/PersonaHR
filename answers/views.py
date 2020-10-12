
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from rest_framework import viewsets

from .models import Answers, Questions, QuestionOptions, Specialization
from .serializers import AnswerSerializer, QuestionSerializer, \
    QuestionOptionSerializer, SpecializationSerializer


class AnswersViewSet(viewsets.ModelViewSet):
    queryset = Answers.objects.all()
    serializer_class = AnswerSerializer


class QuestionsViewSet(viewsets.ModelViewSet):
    queryset = Questions.objects.all()
    serializer_class = QuestionSerializer


class QuestionOptionsViewSet(viewsets.ModelViewSet):
    # queryset = QuestionOptions.objects.all()
    serializer_class = QuestionOptionSerializer

    def get_queryset(self):
        return QuestionOptions.objects.filter(question=self.kwargs[
            'question_pk'])


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer



