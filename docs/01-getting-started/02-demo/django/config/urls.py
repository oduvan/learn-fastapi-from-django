from django.urls import path

from items import views

urlpatterns = [
    path("", views.read_root),
    path("items", views.list_items),
    path("items/<int:item_id>", views.get_item),
]
