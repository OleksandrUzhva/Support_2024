# from django.contrib.auth import get_user_model
# import json
# from django.http import HttpRequest, JsonResponse # noqa
from django.contrib.auth.hashers import make_password
from rest_framework import generics, permissions, serializers, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from .enums import Role
from .models import User

# User = get_user_model() # other method for import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "is_active",
        ]  # noqa

    def validate_role(self, value: str) -> str:
        if value not in Role.users():
            raise ValidationError(
                f"Selected Role must be in {Role.users_value()}"
            )  # noqa
        return value

    def validate(self, attrs):
        attrs["password"] = make_password(attrs["password"])
        return attrs


class UserRegistrationPublickSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role"]


class UserAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.all()

    def post(self, requst):
        serializer = self.get_serializer(data=requst.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            UserRegistrationPublickSerializer(serializer.data).data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data),
        )

    def get(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role in [Role.ADMIN]:
            return True

        return False


class UserRetrieveAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "put", "patch", "delete"]
    serializer_class = UserRegistrationPublickSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = "id"
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        if request.user.role != Role.ADMIN:
            raise PermissionDenied("Only admin users can perform this action.")

        return super().delete(request, *args, **kwargs)

    # def delete(self, request):
    #     # if request.user.role == Role.JUNIOR or Role.SENIOR:
    #     #     raise Exception("Only Admin can delete")

    #     return super().delete(request)


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
