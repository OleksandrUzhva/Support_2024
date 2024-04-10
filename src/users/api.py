# from django.contrib.auth import get_user_model
# import json
# from django.http import HttpRequest, JsonResponse # noqa
from django.contrib.auth.hashers import make_password
from rest_framework import generics, serializers

from .models import User

# User = get_user_model() # other method for import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "is_active"]  # noqa

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        validated_data["password"] = make_password(
            validated_data.get("password")
        )  # noqa
        return super().create(validated_data)


class UserAPI(generics.CreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class UserRetrieveAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "put", "patch", "delete"]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = "id"


# def create_user(request: HttpRequest) -> JsonResponse:
#     if request.method != "POST":
#         raise NotImplementedError("Only POST requests")
#     data: dict = json.loads(request.body)
#     user = User.objects.create_user(**data)
#     # user.pk = None # this method make dublicate
#     # user.save()

#     # convert to dict

#     results = {
#         "id": user.id,
#         "email": user.email,
#         "first_name": user.first_name,
#         "last_name": user.last_name,
#         "role": user.role,
#         "is_active": user.is_active,
#     }

#     return JsonResponse(results)
