import json

from django.http import Http404, HttpRequest, JsonResponse # noqa F401
from django.shortcuts import render  # noqa F401
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from issues.models import Issues


class IssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = ["id", "title", "body", "junior_id", "senior_id"]
        # fields = "__all__" # returne the whole column
        # exclude = ["id"...] # exclude some column which we don`t need

    # def validate(self, attrs):
    #     return super().validate(attrs)


@api_view()
def get_issues(request) -> Response:
    # issue = Issues.objects.get()
    # issue = Issues.objects.update()
    # issue = Issues.objects.delete()
    # issue = Issues.objects.create()
    issues = Issues.objects.all()

    result: list[IssuesSerializer] = [IssuesSerializer(issue).data for issue in issues] # noqa 

    return Response(data=result)


@api_view()
def retrieve_issues(request, issue_id: int) -> Response:
    try:
        issues = Issues.objects.get(id=issue_id)
    # issues = Issues.objects.update()
    # issues = Issues.objects.delete()
    # issues = Issues.objects.create()
    # issues = Issues.objects.all()
    except Issues.DoesNotExist:
        raise Http404
    return Response(data={"result": IssuesSerializer(issues).data})


@api_view(["POST"])
@csrf_exempt
def post_issues(request) -> Response:
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
        # issue = Issues.objects.get()
        # issue = Issues.objects.update()
        # issue = Issues.objects.delete()
        # issue = Issues.objects.all()
        except json.decoder.JSONDecodeError:
            raise Exception("Request Body is invalid")
    serializer = IssuesSerializer(data=payload)
    serializer.is_valid(raise_exception=True)

    issue = Issues.objects.create(**serializer.validated_data)

    return Response(data=IssuesSerializer(issue).data)
