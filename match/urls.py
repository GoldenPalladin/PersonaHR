

'''
from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from django.urls import include
from .views import MatchViewSet

app_name = "match"

router = DefaultRouter()                                 
router.register(r'match', MatchViewSet, basename='match')

urlpatterns = [
    url(r'^', include(router.urls)),
]

'''
from django.urls import path
from .views import match_list

urlpatterns = [
    path('', match_list),
]


'''
from django.urls import path

from .views import MatchView

app_name = 'match'

urlpatterns = [
    path('', MatchView.get, name='index'),
]
'''