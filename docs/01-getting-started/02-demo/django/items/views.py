from django.http import JsonResponse

# In-memory data — the database comes in a later topic.
ITEMS = [
    {"id": 1, "name": "Widget"},
    {"id": 2, "name": "Gadget"},
    {"id": 3, "name": "Gizmo"},
]


def read_root(request):
    return JsonResponse({"message": "It works!"})


def list_items(request):
    limit = int(request.GET.get("limit", 10))  # you convert/validate by hand
    return JsonResponse({"items": ITEMS[:limit]})


def get_item(request, item_id):
    for item in ITEMS:
        if item["id"] == item_id:
            return JsonResponse(item)
    return JsonResponse({"detail": "Item not found"}, status=404)
