from rest_framework import viewsets
from .serializers import PositionSerializer, Position


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
