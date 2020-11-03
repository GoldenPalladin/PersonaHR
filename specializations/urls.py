from django.urls import include, path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import QuestionsViewSet, \
    QuestionOptionsViewSet, SpecializationViewSet

app_name = 'specializations'

router = DefaultRouter()
router.register(r'questions', QuestionsViewSet, basename='questions')
router.register(r'specializations', SpecializationViewSet)

questions_router = routers.NestedDefaultRouter(router, r'questions',
                                               lookup='question')
questions_router.register(r'options', QuestionOptionsViewSet,
                          basename='options')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(questions_router.urls)),
]
