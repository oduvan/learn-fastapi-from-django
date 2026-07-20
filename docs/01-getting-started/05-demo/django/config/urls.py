from django.urls import path

from core import views

urlpatterns = [
    path("users", views.list_users),
    path("health", views.health),
]
