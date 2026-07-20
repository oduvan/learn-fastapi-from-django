from django.http import JsonResponse

from core import pool


def list_users(request):
    return JsonResponse({"users": pool.pool.get_users()})


def health(request):
    return JsonResponse({"status": "ok"})
