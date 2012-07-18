'''
Created on 9. 7. 2012.

@author: ihabunek
'''
from divelog.models import Dive, DiveUpload, Location
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.forms.models import ModelForm

class DiveForm(ModelForm):
    class Meta:
        model = Dive
        exclude = ('number', 'fingerprint', 'size', 'user')

class DiveUploadForm(ModelForm):
    class Meta:
        model = DiveUpload
        exclude = ('uploaded', 'user')

class LocationForm(ModelForm):
    class Meta:
        model = Location
        exclude = ('user')

class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ValidatingPasswordChangeForm(PasswordChangeForm):
    """
    A password change form which adds password validation. Currently only 
    checks min length.
    """
    MIN_LENGTH = 8

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')

        if len(password1) < self.MIN_LENGTH:
            raise forms.ValidationError("The new password must be at least %d characters long." % self.MIN_LENGTH)

        return password1

