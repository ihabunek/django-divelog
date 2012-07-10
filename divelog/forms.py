'''
Created on 9. 7. 2012.

@author: ihabunek
'''
from django.forms.models import ModelForm
from django import forms
from divelog.models import Dive

class DiveForm(ModelForm):
    class Meta:
        model = Dive
        exclude = ('number', 'fingerprint', 'size', 'user')
        
class UploadFileForm(forms.Form):
    file = forms.FileField()
