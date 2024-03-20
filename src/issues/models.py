from django.db import models


class Issues(models.Model):
    junior_id = models.IntegerField()
    senior_id = models.IntegerField()
    titel = models.CharField(max_length=100)
    body = models.TextField()
