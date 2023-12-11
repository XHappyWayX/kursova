from django.db import models
from django.contrib.auth.models import User

class resource(models.Model):
    resource_name = models.CharField(max_length=255, default='')
    unit_price = models.FloatField(default=0)
    consumed_per_month = models.FloatField(default=0)
    expenses_for_the_month = models.FloatField(default=0)

class CustomUser(User):
    date_of_birth = models.DateField(null=True, blank=True)