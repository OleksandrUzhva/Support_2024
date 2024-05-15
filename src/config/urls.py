from django.contrib import admin  # noqa
from django.urls import path  # noqa
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import token_obtain_pair  # noqa

from issues.api import IssueAPI  # noqa
from issues.api import IssuesRetrieveAPI  # noqa
from issues.api import issues_close  # noqa
from issues.api import issues_take  # noqa
from issues.api import messages_api_dispatcher  # noqa; noqa
from users.api import UserActivationAPI, UserAPI, UserRetrieveAPI  # noqa

# from rest_framework_simplejwt.views import TokenObtainPairView  # noqa

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # admin
    path("admin/", admin.site.urls),
    # users
    path("users/", UserAPI.as_view()),
    path("users/<int:id>", UserRetrieveAPI.as_view()),
    path("users/activate/", UserActivationAPI.as_view()),
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
    path(
        "swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/", schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc"
    ),
]
