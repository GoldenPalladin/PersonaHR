from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import Skill, Response, SkillSerialiser, SkillsSerialiser


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerialiser


class SkillsViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = SkillsSerialiser
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['skill']
