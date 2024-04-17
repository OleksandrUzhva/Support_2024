# from django.http import Http404, HttpRequest, JsonResponse  # noqa F401
# from django.shortcuts import render  # noqa F401
from django.db.models import Q
from rest_framework import generics, permissions, response, serializers  # noqa
from rest_framework.decorators import api_view, permission_classes  # noqa
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from users.enums import Role

from .enums import Status
from .models import Issue, Message

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
            return Issue.objects.filter(
                Q(senior=user) | (Q(senior=None) & Q(Status=Status.OPEND))
            )
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
    permission_classes = [IsAdminOrSeniorUser]  # noqa F811

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


# CBV
# ===========================================================

# class MessageCreateAPI(generics.CreateAPIView):
#     serializer_class = MessegaSerializer

# class MessageListApi(generics.RetrieveAPIView):
#     lookup_url_kwarg = "id"
#     serializer_class = MessegaSerializer

#     def get_queryset(self):
#         return Message.objects.filter(issue__id = self.request)
# =================================================================


class MessegaSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())

    class Meta:
        model = Message
        fields = "__all__"

    def save(self):
        if (user := self.validated_data.pop("user", None)) is not None:
            self.validated_data["user_id"] = user.id
        if (issue := self.validated_data.pop("issue", None)) is not None:
            self.validated_data["issue_id"] = issue.id
        return super().save()


@api_view(["GET", "POST"])
def messages_api_dispatcher(request: Request, issue_id: int):
    if request.method == "GET":
        # messages = Message.objects.filter(
        # Q(
        #     issue__id=issue_id,
        #     issue__junior = request.user
        # )
        # | Q(
        #     issue__id = issue_id,
        #     issue__senior = request.user
        # )
        messages = Message.objects.filter(
            Q(issue__id=issue_id)
            & (Q(issue__senior=request.user) | Q(issue__junior=request.user))
        ).order_by("-timestamp")
        serializers = MessegaSerializer(messages, many=True)

        return response.Response(serializers.data)
    else:
        issue = Issue.objects.get(id=issue_id)
        payload = request.data | {"issue": issue.id}

        serializer = MessegaSerializer(
            data=payload, context={"request": request}
        )  # noqa
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.validated_data)


# Other method for permissons:
# class UserRelatedToIssue(permissions.BasePermission):

#     def has_object_permission(self, request, view, obj):
#         return super().has_object_permission(request, view, obj)


@api_view(["PUT"])
# @permission_classes([UserRelatedToIssue])
def issues_close(request: Request, id: int):
    issue = Issue.objects.get(id=id)
    if request.user.role != Role.SENIOR:
        raise PermissionError("Only senior can close issues")  # noqa

    if issue.status != Status.IN_PROGRESS:
        raise response.Response(
            {"message": "Issue is not In progress..."}, status=422
        )  # noqa
    else:
        issue.senior = request.user
        issue.status = Status.CLOSED
        issue.save()

    serializers = IssuesSerializer(issue)
    return response.Response(serializers.data)


@api_view(["PUT"])
def issues_take(request: Request, id: int):
    issue = Issue.objects.get(id=id)

    if request.user.role != Role.SENIOR:
        raise PermissionError("Only senior users can take issues")

    if (issue.status != Status.OPEND) or (issue.senior is not None):
        raise response.Response(
            {"message": "Issue is not Opend or senior is set..."}, status=422
        )
    else:
        issue.senior = request.user
        issue.status = Status.IN_PROGRESS
        issue.save()

    serializers = IssuesSerializer(issue)

    return response.Response(serializers.data)


# FBV
# =====================================================
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
# ========================================================================
