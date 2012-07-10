from django.contrib.auth.models import User
from django.db import models

class Dive(models.Model):
    user = models.ForeignKey(User)
    number = models.IntegerField()
    size = models.IntegerField()
    fingerprint = models.CharField(max_length = 32)
    max_depth = models.FloatField()
    date_time = models.DateTimeField()
    duration = models.IntegerField()
    comment = models.TextField(default='')

class Sample(models.Model):
    dive = models.ForeignKey(Dive)
    time = models.IntegerField()
    depth = models.FloatField()
    temperature = models.FloatField(null=True)
    
class Event(models.Model):
    dive = models.ForeignKey(Dive)
    time = models.IntegerField()
    text = models.CharField(max_length = 128)

class DiveUpload(models.Model):
    user = models.ForeignKey(User)
    data = models.FileField(upload_to = 'uploads/%Y%m')
    uploaded = models.DateTimeField()
