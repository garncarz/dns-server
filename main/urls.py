from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('', include('dns.urls', namespace='dns')),
    path('admin/', admin.site.urls),
]
