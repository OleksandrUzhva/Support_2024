from django.db import models

from users.models import User


class Issue(models.Model):
    title = models.CharField(max_length=100)
    status = models.PositiveSmallIntegerField()

    junior = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="junior_issue"
    )
    senior = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="senior_issue", null=True
    )


class Massege(models.Model):
    body = models.TextField
    timestamp = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_massege"
    )
    issue = models.ForeignKey(
        Issue, on_delete=models.CASCADE, related_name="issue_massege"
    )
