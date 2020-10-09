
from rest_framework.routers import DefaultRouter

from .views import AnswersViewSet, QuestionsViewSet, QuestionOptionsViewSet

app_name = "articles"

router = DefaultRouter()

router.register(r'answers', AnswersViewSet)
router.register(r'questions', QuestionsViewSet)
router.register(r'options', QuestionOptionsViewSet)

urlpatterns = router.urls



