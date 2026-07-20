from django.urls import path

from . import views

urlpatterns = [
    path("users", views.list_users),
    path("users/<int:user_id>", views.get_user),
]
