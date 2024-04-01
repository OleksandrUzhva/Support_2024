from django.contrib import admin
from django.urls import path

from issues.api import get_issues, post_issues, retrieve_issues

urlpatterns = [
    path("admin/", admin.site.urls),
    path("issues/", get_issues),
    path("issues/<int:issue_id>", retrieve_issues),
    path("issues/create", post_issues),
]
