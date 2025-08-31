from django.urls import path, include, re_path
from rest_framework import routers

from . import views

api_router = routers.DefaultRouter()
api_router.register(r'record', views.RecordViewSet)

app_name = 'dns'

urlpatterns = [
    path('api/', include((api_router.urls, 'api'))),
    re_path(r'^links/(?P<abbr>.*)', views.redirection),
]
