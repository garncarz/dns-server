from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('dns.urls', namespace='dns')),
    url(r'^', admin.site.urls),
]
