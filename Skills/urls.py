from django.urls import include, path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import SkillViewSet, SkillResponsesViewSet

app_name = 'skills'

router = DefaultRouter()
router.register(r'skill', SkillViewSet, basename='skill')
router.register(r'response', SkillResponsesViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]