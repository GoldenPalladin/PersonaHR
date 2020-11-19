from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from django.urls import include
from .views import AnswersViewSet, SkillResponsesViewSet

app_name = "answers"

router = DefaultRouter()
router.register(r'answers', AnswersViewSet)
router.register(r'skills', SkillResponsesViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]



