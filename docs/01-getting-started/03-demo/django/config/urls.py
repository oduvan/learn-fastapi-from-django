from django.urls import path

from core import views

urlpatterns = [
    path("", views.read_root),
    path("health", views.health),
]
