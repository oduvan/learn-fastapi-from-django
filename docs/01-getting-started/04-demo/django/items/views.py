from django.http import JsonResponse

ITEMS = [
    {"id": 1, "name": "Widget"},
    {"id": 2, "name": "Gadget"},
]


def list_items(request):
    return JsonResponse({"items": ITEMS})


def get_item(request, item_id):
    for item in ITEMS:
        if item["id"] == item_id:
            return JsonResponse(item)
    return JsonResponse({"detail": "Item not found"}, status=404)
