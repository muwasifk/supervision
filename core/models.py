"""
models.py
ICS4U SDP 
Muhammad Wasif Kamran, Karan Chawla, Eric Sui 
Classes to represent Django models / tables in database 
"""
# Django imports
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

class Schedule(models.Model):
    """
    Model to represent a schedule 
    """
    schedule_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    school = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)


class Teacher(models.Model):
    """
    Model to represent a teacher
    """
    schedule_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    contract = models.CharField(max_length=255)
    schedule = models.CharField(max_length=255)


class ScheduleList(models.Model):
    """
    Model to represent a list of schedules 
    """
    email = models.EmailField(max_length=255)
    schedules = ArrayField(models.CharField(max_length=255), size=0)
