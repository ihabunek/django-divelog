from divelog.models import Dive, DiveUpload, Location
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from django.forms.util import ErrorList
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode

class BootstrapErrorList(ErrorList):
    def __unicode__(self):
        return self.as_text()

    def as_text(self):
        if not self: return u''
        errors = '<br />'.join(conditional_escape(force_unicode(e)) for e in self)
        return mark_safe(u'<span class="help-inline">%s</span>' % errors)

class BootstrapModelForm(ModelForm):
    '''
    Overrides the default model form and does the following:
    - sets the error_class to BootstrapErrorList
    '''
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None,
                 error_class=BootstrapErrorList, label_suffix=':', empty_permitted=False,
                 instance=None):
        super(BootstrapModelForm, self).__init__(data, files, auto_id, prefix, initial,
                                                 error_class, label_suffix, empty_permitted,
                                                 instance)

class DiveForm(BootstrapModelForm):
    class Meta:
        model = Dive
        exclude = ('number', 'fingerprint', 'size', 'user')

class DiveUploadForm(BootstrapModelForm):
    class Meta:
        model = DiveUpload
        exclude = ('uploaded', 'user')

class LocationForm(BootstrapModelForm):
    class Meta:
        model = Location
        exclude = ('user')

class UserProfileForm(BootstrapModelForm):
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

