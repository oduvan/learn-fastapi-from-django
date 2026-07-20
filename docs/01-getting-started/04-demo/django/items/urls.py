from django.urls import path

from . import views

urlpatterns = [
    path("items", views.list_items),
    path("items/<int:item_id>", views.get_item),
]
