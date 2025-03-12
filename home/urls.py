from django.urls import path
from  . import views
from django.contrib import admin

urlpatterns = [
    #rota para view index
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
]
