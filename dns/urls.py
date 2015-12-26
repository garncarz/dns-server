from django.conf.urls import url, include
from rest_framework import routers

from . import views

api_router = routers.DefaultRouter()
api_router.register(r'record', views.RecordViewSet)

urlpatterns = [
    url(r'^api/', include(api_router.urls, namespace='api')),
]
