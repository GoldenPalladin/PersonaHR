from rest_framework import viewsets

from .models import Answers
from .serializers import AnswerSerializer


class AnswersViewSet(viewsets.ModelViewSet):
    queryset = Answers.objects.all()
    serializer_class = AnswerSerializer






