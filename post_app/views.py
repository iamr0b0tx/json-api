from django.http import JsonResponse


# Create your views here.
def ping(request):
    return JsonResponse({
        "success": True
    })


def get_posts(request):
    return JsonResponse({
        "success": True
    })
