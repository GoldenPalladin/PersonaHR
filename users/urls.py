from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from django.urls import include, path
from .views import UserProfileViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]