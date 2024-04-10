from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


class Schedule(models.Model):
    schedule_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    school = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)


class Teacher(models.Model):
    schedule_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    contract = models.CharField(max_length=255)
    schedule = models.CharField(max_length=255)


class ScheduleList(models.Model):
    email = models.EmailField(max_length=255)
    schedules = ArrayField(models.CharField(max_length=255), size=0)
