from operator import index
from . import views
from django.contrib import admin
from django.urls import path
 
 
urlpatterns = [
    path("predict/", views.predict, name='predict'),
    path("predict/result", views.result),
    path('logout/', views.logout_view, name='logout'),
    path('', views.login_view, name='login'),
    path('add_account/', views.add_account_view, name='add_account'),
]

