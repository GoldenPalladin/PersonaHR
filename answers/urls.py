from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from rest_framework.schemas import get_schema_view
from django.urls import include, path
from rest_framework_nested import routers
from .views import AnswersViewSet, QuestionsViewSet, QuestionOptionsViewSet, SpecializationViewSet

app_name = "articles"

router = DefaultRouter()

schema_view = get_schema_view(title='Persona API',
                              description='An API to match employers and '
                                          'candidates.')

router.register(r'answers', AnswersViewSet)
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



