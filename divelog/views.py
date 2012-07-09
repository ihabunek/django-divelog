from divelog.models import Dive, DiveForm

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.template import loader
from django.template.context import RequestContext
from datetime import timedelta
from time import mktime
import logging

def index(request):
    t = loader.get_template('divelog/index.html')
    c = RequestContext(request);
    return HttpResponse(t.render(c))

@login_required
def dives(request):
    """
    Displays a list of user's dives.
    """
    dives = Dive.objects.all()

    t = loader.get_template('divelog/dives.html')
    c = RequestContext(request, {
        'dives': dives,
        'user': request.user
    });
    return HttpResponse(t.render(c))

@login_required
def dives_import(request):
	pass
	
@login_required
def dive(request, dive_id):
    try:
        dive = Dive.objects.get(pk = dive_id)
    except Dive.DoesNotExist:
        raise Http404
    
    # Prepare chart data
    chart = {
        'depth': [],
        'temperature': [],
        'events': []
    }
    
    last_temp = None
    
    for sample in dive.sample_set.all():
        delta = timedelta(seconds = sample.time)
        sample_time = dive.date_time + delta
        sample_ts = int(1000 * mktime(sample_time.timetuple()))
        
        if sample.temperature:
            last_temp = sample.temperature
        
        chart['depth'].append([sample_ts, sample.depth])
        chart['temperature'].append([sample_ts, last_temp])
        
    for event in dive.event_set.all():
        delta = timedelta(seconds = event.time)
        event_time = dive.date_time + delta
        chart['events'].append({
            'x': int(1000 * mktime(event_time.timetuple())),
            'title': event.text
        })
    
    t = loader.get_template('divelog/dive.html')
    c = RequestContext(request, {
        'dive': dive,
        'chart': chart
    });
    return HttpResponse(t.render(c))

@login_required
def dive_edit(request, dive_id):
    dive_url = '/dive/%d' % int(dive_id)
    
    if request.method == 'POST':
        dive = Dive.objects.get(pk = dive_id)
        form = DiveForm(request.POST, instance = dive)
        if form.is_valid():
            form.save()
            return redirect('divelog.views.dive', dive_id = dive_id)
    else:
        dive = Dive.objects.get(pk = dive_id)
        form = DiveForm(instance = dive)
    
    t = loader.get_template('divelog/dive_edit.html')
    c = RequestContext(request, {
        'form': form,
        'dive_id': dive_id,
        'dive_url': dive_url,
    });
    return HttpResponse(t.render(c))

@login_required
def profile(request):
    t = loader.get_template('accounts/profile.html')
    c = RequestContext(request, {
    });
    return HttpResponse(t.render(c))
	
	
@login_required
def edit_dive(request):
    """
    Displays a list of user's dives.
    """
    dives = Dive.objects.all()

    t = loader.get_template('divelog/dives.html')
    c = RequestContext(request, {
        'dives': dives,
        'user': request.user
    });
    return HttpResponse(t.render(c))
