from django.http import Http404, HttpRequest, JsonResponse  # noqa F401
from django.shortcuts import render  # noqa F401
from rest_framework import generics, serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from users.enums import Role

from .enums import Status
from .models import Issue

# from django.http import HttpRequest, JsonResponse # noqa
# from rest_framework.decorators import api_view
# from rest_framework.response import Response


# class IssueCreatSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Issue
#         fields = ["id", "title", "body"]

#     def validate(self, attrs):
#         request = self.context["request"]
#         attrs["status"] = Status.OPEND
#         # attrs["junior"] = request.user
#         return attrs


class IssuesSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False)
    junior = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Issue
        fields = ["id", "title", "status", "body", "junior", "senior"]
        # fields = "__all__" # returne the whole column
        # exclude = ["id"...] # exclude some column which we don`t need

    # def validate(self, attrs):
    #     return super().validate(attrs)

    def validate(self, attrs):
        # request = self.context["request"]
        attrs["status"] = Status.OPEND
        # attrs["junior"] = request.user
        return attrs


class IssueAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = IssuesSerializer

    # def get_serializer_class(self):
    #     if self.request.method == "POST":
    #         return IssueCreatSerializer
    #     else:
    #         return IssuesSerializer
    def get_queryset(self):
        user = self.request.user
        if user.role == Role.ADMIN:
            return Issue.objects.all()
        elif user.role == Role.SENIOR:
            return Issue.objects.filter(senior=user).exclude(
                junior__role=Role.SENIOR
            )  # noqa
        elif user.role == Role.JUNIOR:
            return Issue.objects.filter(junior=user)

    def post(self, request):
        if request.user.role != Role.SENIOR:
            raise Exception("The role is senior")
        return super().post(request)


class IsAdminOrSeniorUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role in [Role.ADMIN, Role.SENIOR]:
            return True

        return False


class IssuesRetrieveAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "put", "patch", "delete"]
    serializer_class = IssuesSerializer
    queryset = Issue.objects.all()
    lookup_url_kwarg = "id"
    permission_classes = [IsAdminOrSeniorUser]

    def put(self, request, *args, **kwargs):
        if request.user.role == Role.JUNIOR:
            raise PermissionDenied(
                "Only Admin or Senior users can perform this action."
            )

        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if request.user.role != Role.ADMIN:
            raise PermissionDenied("Only admin users can perform this action.")

        return super().delete(request, *args, **kwargs)


# @api_view()
# def get_issues(request) -> Response:
#     # issue = Issue.objects.get()
#     # issue = Issue.objects.update()
#     # issue = Issue.objects.delete()
#     # issue = Issue.objects.create()
#     issues = Issue.objects.all()

#     result: list[IssuesSerializer] = [
#         IssuesSerializer(issue).data for issue in issues
#     ]  # noqa

#     return Response(data={"result": result})


# @api_view()
# def retrieve_issues(request, issue_id: int) -> Response:
#     try:
#         issues = Issue.objects.get(id=issue_id)
#     # issues = Issue.objects.update()
#     # issues = Issue.objects.delete()
#     # issues = Issue.objects.create()
#     # issues = Issue.objects.all()
#     except Issue.DoesNotExist:
#         raise Http404
#     return Response(data={"result": IssuesSerializer(issues).data})
