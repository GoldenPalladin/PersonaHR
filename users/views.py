from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import UserProfile, UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['userType']
