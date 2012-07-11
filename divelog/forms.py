'''
Created on 9. 7. 2012.

@author: ihabunek
'''
from divelog.models import Dive, DiveUpload
from django import forms
from django.forms.models import ModelForm

class DiveForm(ModelForm):
    class Meta:
        model = Dive
        exclude = ('number', 'fingerprint', 'size', 'user')
#        widgets = {
#            'duration': TimeInput(format="%H:%M"),
#        }

class DiveUploadForm(ModelForm):
    class Meta:
        model = DiveUpload
        exclude = ('uploaded', 'user')
        
        
class UploadFileForm(forms.Form):
    file = forms.FileField()
