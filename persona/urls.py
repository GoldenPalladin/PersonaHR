"""persona URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from allauth.account.views import confirm_email
from .views import redirect_to_docs

schema_view = get_schema_view(
    openapi.Info(
        title="Persona API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="p.yakovlev@live.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', redirect_to_docs),
    path('admin/', admin.site.urls),
    path('api/answers/', include('answers.urls')),
    path('api/specializations/', include('specializations.urls')),
    path('api/users/', include('users.urls')),
    path('api/skills/', include('Skills.urls')),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^rest-auth/registration/account-confirm-email/(?P<key>.+)/$',
        confirm_email, name='account_confirm_email'),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]
