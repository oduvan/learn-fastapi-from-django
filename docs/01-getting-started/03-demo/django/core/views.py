from django.http import JsonResponse


def read_root(request):
    return JsonResponse({"message": "It works!"})


def health(request):
    return JsonResponse({"status": "ok"})
