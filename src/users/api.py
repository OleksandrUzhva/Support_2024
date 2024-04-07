# from django.contrib.auth import get_user_model
import json

from django.http import HttpRequest, JsonResponse

from .models import User

# User = get_user_model() # other method for import User


def create_user(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        raise NotImplementedError("Only POST requests")
    data: dict = json.loads(request.body)
    user = User.objects.create_user(**data)
    # user.pk = None # this method make dublicate
    # user.save()

    # convert to dict

    results = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "is_active": user.is_active,
    }

    return JsonResponse(results)
