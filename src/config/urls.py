from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView  # noqa
from rest_framework_simplejwt.views import token_obtain_pair

from issues.api import get_issues, post_issues, retrieve_issues
from users.api import create_user

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", create_user),
    path("issues/", get_issues),
    path("issues/<int:issue_id>", retrieve_issues),
    path("issues/create", post_issues),
    # Authentication
    path("auth/token/", token_obtain_pair)
    # path("auth/token/", TokenObtainPairView.as_view())
]
