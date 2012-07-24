from divelog.forms import UserProfileForm, ValidatingPasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.template.context import RequestContext

def index(request):
    t = loader.get_template('divelog/index.html')
    c = RequestContext(request);
    return HttpResponse(t.render(c))

def gallery(request):
    t = loader.get_template('divelog/gallery.html')
    c = RequestContext(request);
    return HttpResponse(t.render(c))

@login_required
def settings(request):
    return redirect('divelog_settings_account')

@login_required
def settings_account(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your settings have been saved.")
    else:
        form = UserProfileForm(instance=request.user)
    
    t = loader.get_template('divelog/settings/account.html')
    c = RequestContext(request, {
        'form': form,
    });
    return HttpResponse(t.render(c))

@login_required
def settings_password(request):
    if request.method == 'POST':
        form = ValidatingPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed.")
    else:
        form = ValidatingPasswordChangeForm(request.user)
    
    t = loader.get_template('divelog/settings/password.html')
    c = RequestContext(request, {
        'form': form,
    });
    return HttpResponse(t.render(c))
