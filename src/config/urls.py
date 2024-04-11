from django.contrib import admin  # noqa
from django.urls import path  # noqa
from rest_framework_simplejwt.views import token_obtain_pair  # noqa

from issues.api import IssueAPI, IssuesRetrieveAPI  # noqa
from users.api import UserAPI, UserRetrieveAPI  # noqa

# from rest_framework_simplejwt.views import TokenObtainPairView  # noqa
# dfsdfsd
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
