from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView  # noqa
from rest_framework_simplejwt.views import token_obtain_pair  # noqa

from issues.api import IssueAPI, IssuesRetrieveAPI
from users.api import UserAPI, UserRetrieveAPI

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", UserAPI.as_view()),
    path("users/<int:id>", UserRetrieveAPI.as_view()),
    path("issues/", IssueAPI.as_view()),
    path("issues/<int:id>", IssuesRetrieveAPI.as_view()),
    # Authentication
    path("auth/token/", token_obtain_pair)
    # path("auth/token/", TokenObtainPairView.as_view())
]
