from django.http import JsonResponse

USERS = [
    {"id": 1, "name": "Ada"},
    {"id": 2, "name": "Alan"},
]


def list_users(request):
    return JsonResponse({"users": USERS})


def get_user(request, user_id):
    for user in USERS:
        if user["id"] == user_id:
            return JsonResponse(user)
    return JsonResponse({"detail": "User not found"}, status=404)
