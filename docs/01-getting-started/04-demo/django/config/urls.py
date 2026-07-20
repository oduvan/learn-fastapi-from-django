from django.urls import include, path

from config import views

urlpatterns = [
    path("", views.read_root),
    path("", include("items.urls")),
    path("", include("users.urls")),
]
