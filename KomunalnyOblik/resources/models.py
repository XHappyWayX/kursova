from django.db import models
from django.contrib.auth.models import User


class Resource(models.Model):
    resource_name = models.CharField(max_length=255, default='')
    unit_price = models.FloatField(default=0)
    consumed_per_month = models.FloatField(default=0)
    expenses_per_month = models.FloatField(default=0)
    month = models.CharField(max_length=20, default='')


class CustomUser(User):
    role_id = models.IntegerField(default=0)


class Role(models.Model):
    role_name = models.CharField(max_length=255, default='')