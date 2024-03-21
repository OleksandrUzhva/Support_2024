import json

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render  # noqa F401
from django.views.decorators.csrf import csrf_exempt

from issues.models import Issues


def get_issues(requesst: HttpRequest) -> JsonResponse:
    issue = Issues.objects.get()
    # issue = Issues.objects.update()
    # issue = Issues.objects.delete()
    # issue = Issues.objects.create()
    # issue = Issues.objects.all()

    result = {
        "id": issue.id,
        "titel": issue.titel,
        "body": issue.body,
        "junior_id": issue.junior_id,
        "senior_id": issue.senior_id,
    }

    return JsonResponse(data=result)


@csrf_exempt
def post_issues(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        data = json.loads(request.body)
        titel = data.get("titel")
        body = data.get("body")
    # issue = Issues.objects.get()
    # issue = Issues.objects.update()
    # issue = Issues.objects.delete()
    issue = Issues.objects.create(
        titel=titel,
        body=body,
        junior_id=2,
        senior_id=1,  # noqa E501
    )
    # issue = Issues.objects.all()

    result = {
        "id": issue.id,
        "titel": issue.titel,
        "body": issue.body,
        "junior_id": issue.junior_id,
        "senior_id": issue.senior_id,
    }

    return JsonResponse(data=result)
