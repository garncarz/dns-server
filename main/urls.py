from django.urls import re_path, include
from django.contrib import admin

urlpatterns = [
    re_path(r'^', include(('dns.urls', 'dns'))),
    re_path(r'^', admin.site.urls),
]
