'''
Created on 9. 7. 2012.

@author: ihabunek
'''
from django.forms.models import ModelForm
from django import forms
from divelog.models import Dive, DiveUpload

class DiveForm(ModelForm):
    class Meta:
        model = Dive
        exclude = ('number', 'fingerprint', 'size', 'user')

class DiveUploadForm(ModelForm):
    class Meta:
        model = DiveUpload
        exclude = ('uploaded', 'user')
        
class UploadFileForm(forms.Form):
    file = forms.FileField()
