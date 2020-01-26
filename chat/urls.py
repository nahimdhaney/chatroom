from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('users/login/', views.login_view, name='login'),
    path('users/logout/', views.logout_view, name='logout')

]
