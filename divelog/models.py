from django.db import models
from django.forms.models import ModelForm
from django.contrib.auth.models import User

class Dive(models.Model):
    user = models.ForeignKey(User)
    number = models.IntegerField()
    size = models.IntegerField()
    fingerprint = models.CharField(max_length = 32)
    max_depth = models.FloatField()
    date_time = models.DateTimeField()
    duration = models.IntegerField()

class Sample(models.Model):
    dive = models.ForeignKey(Dive)
    time = models.IntegerField()
    depth = models.FloatField()
    temperature = models.FloatField(null=True)
    
class Event(models.Model):
    dive = models.ForeignKey(Dive)
    time = models.IntegerField()
    text = models.CharField(max_length = 128)

class DiveForm(ModelForm):
    class Meta:
        model = Dive
        exclude = ('number', 'fingerprint', 'size')
        