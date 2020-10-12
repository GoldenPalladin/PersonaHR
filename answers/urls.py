
from rest_framework.routers import DefaultRouter

from .views import AnswersViewSet, QuestionsViewSet, QuestionOptionsViewSet, SpecializationViewSet

app_name = "articles"

router = DefaultRouter()

router.register(r'answers', AnswersViewSet)
router.register(r'questions', QuestionsViewSet)
router.register(r'options', QuestionOptionsViewSet)
router.register(r'specializations', SpecializationViewSet)

urlpatterns = router.urls



