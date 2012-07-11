from django.contrib.auth.models import User
from django.db import models

DIVE_STATUS_CHOICES = (
    ('A', 'Active'),
    ('D', 'Deleted')                      
)

DIVE_STATUS_DEFAULT = 'A'

class Dive(models.Model):
    user = models.ForeignKey(User)
    number = models.IntegerField(default = 0)
    size = models.IntegerField(default = 0)
    fingerprint = models.CharField(max_length = 32, blank = True)
    max_depth = models.FloatField(blank = True)
    date_time = models.DateTimeField(blank = True)
    duration = models.IntegerField(blank = True)
    comment = models.TextField(blank = True)
    status = models.CharField(
        max_length = 1, 
        choices = DIVE_STATUS_CHOICES, 
        default = DIVE_STATUS_DEFAULT
    )
    
    def __unicode__(self):
        return "Dive #%d" % self.id 

class Sample(models.Model):
    dive = models.ForeignKey(Dive)
    time = models.IntegerField()
    depth = models.FloatField()
    temperature = models.FloatField(null=True)
    
    def __unicode__(self):
        return "Sample #%d" % self.id 
    
class Event(models.Model):
    dive = models.ForeignKey(Dive)
    time = models.IntegerField()
    text = models.CharField(max_length = 128)

class DiveUpload(models.Model):
    user = models.ForeignKey(User)
    data = models.FileField(upload_to = 'uploads/%Y%m')
    uploaded = models.DateTimeField()

class Location(models.Model):
    pass

