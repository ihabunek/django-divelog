from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.aggregates import Avg, Max, Min

class Location(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=256)
    lat = models.FloatField(blank = True, null = True, verbose_name = "Latitude")
    lon = models.FloatField(blank = True, null = True, verbose_name = "Longitude")
    def __unicode__(self):
        return self.name

class Dive(models.Model):
    ACTIVE = 'A'
    DEFUNCT = 'D'

    STATUS_CHOICES = (
        (ACTIVE, _('Active')),
        (DEFUNCT, _('Trashed'))
    )
    user = models.ForeignKey(User)
    number = models.IntegerField(default = 0)
    size = models.IntegerField(default = 0)
    fingerprint = models.CharField(max_length = 32, blank = True)
    location = models.ForeignKey(Location, blank=True, null=True)
    max_depth = models.FloatField(blank = True, null = True)
    avg_depth = models.FloatField(blank = True, null = True)
    date_time = models.DateTimeField(blank = True, null = True)
    temperature = models.FloatField(blank = True, null = True)
    duration = models.IntegerField(null = True)
    comment = models.TextField(blank = True)
    status = models.CharField(max_length = 1,
        choices = STATUS_CHOICES,
        default = ACTIVE
    )
    
    def trash(self):
        self.status = self.DEFUNCT
        self.save()
    
    def restore(self):
        self.status = self.ACTIVE
        self.save()
    
    class Meta:
        ordering = ['-date_time']

def dive_stats(dive_id):
    "Calculates dive statistics from it's sample data."
    return Sample.objects.filter(dive_id=dive_id).aggregate(
        avg_depth = Avg('depth'),
        max_depth = Max('depth'),
        min_temp = Min('temperature'),
        max_temp = Max('temperature'),
        avg_temp = Avg('temperature'),
        duration = Max('time'),
    )

class Sample(models.Model):
    dive = models.ForeignKey(Dive)
    time = models.IntegerField()
    depth = models.FloatField()
    temperature = models.FloatField(null=True)
    pressure = models.FloatField(null=True)
    
class Event(models.Model):
    dive = models.ForeignKey(Dive)
    time = models.IntegerField()
    text = models.CharField(max_length = 128)
    
class DiveUpload(models.Model):
    user = models.ForeignKey(User)
    data = models.FileField(upload_to = 'uploads/%Y%m')
    uploaded = models.DateTimeField()
