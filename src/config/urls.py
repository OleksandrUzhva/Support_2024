from django.contrib import admin  # noqa
from django.urls import path  # noqa
from rest_framework_simplejwt.views import token_obtain_pair  # noqa

from issues.api import (
    IssueAPI,
    IssuesRetrieveAPI,
    issues_close,
    issues_take,
    messages_api_dispatcher,
)
from users.api import UserAPI, UserRetrieveAPI  # noqa

# from rest_framework_simplejwt.views import TokenObtainPairView  # noqa
# dfsdfsd
urlpatterns = [
    # admin
    path("admin/", admin.site.urls),
    # users
    path("users/", UserAPI.as_view()),
    path("users/<int:id>", UserRetrieveAPI.as_view()),
    # issues
    path("issues/", IssueAPI.as_view()),
    path("issues/<int:id>", IssuesRetrieveAPI.as_view()),
    path("issue/<int:id>/close", issues_close),
    path("issue/<int:id>/take", issues_take),
    # messages
    path("issue/<int:issue_id>/message", messages_api_dispatcher),
    # Authentication
    path("auth/token/", token_obtain_pair),
    # path("auth/token/", TokenObtainPairView.as_view())
]
