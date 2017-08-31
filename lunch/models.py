#coding:utf-8
from __future__ import unicode_literals

from django.db import models
import uuid
import datetime
from django.utils import timezone
import time
# Create your models here.


class Activity(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    activity_name = models.CharField(max_length=50)
    food_selects = models.CharField(max_length=255)
    create_date = models.DateField(default=datetime.date.today)
    biller_ip = models.GenericIPAddressField(null=True)
    biller_name = models.CharField(max_length=50, null=True)


class RollRecord(models.Model):
    name = models.CharField(max_length=50)
    food = models.CharField(max_length=50)
    user_ip = models.CharField(max_length=50)
    num = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    # bill = models.DecimalField(max_digits=3, decimal_places=2)
    is_payed = models.BooleanField(default=False)
    uuid = models.ForeignKey(Activity)




