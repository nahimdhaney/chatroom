"""chatroom URL Configuration
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from chat.views import index

urlpatterns = [
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
]
