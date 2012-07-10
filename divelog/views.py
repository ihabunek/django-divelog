from datetime import timedelta
from divelog.forms import DiveForm, UploadFileForm
from divelog.models import Dive
from divelog.parsers.libdc import parse_short
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.template import loader
from django.template.context import RequestContext
from time import mktime
import logging

def index(request):
    """
    Title page view.
    """
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
        'dives': dives
    });
    return HttpResponse(t.render(c))

@login_required
def upload(request):
    """
    Allows user to upload dive computer data. 
    """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            ffile = request.FILES['file']
            dive_data = '<dives>' + ffile.read() + '</dives>' # fix broken libdc xml format
            dives = parse_short(dive_data)
        else:
            raise Exception("Error uploading file")

        t = loader.get_template('divelog/upload_review.html')
        c = RequestContext(request, {
            'file': ffile,
            'dives': dives
        });
        return HttpResponse(t.render(c))

    else:
        form = UploadFileForm()
        t = loader.get_template('divelog/upload.html')
        c = RequestContext(request, {
            'form': form
        });
        return HttpResponse(t.render(c))

@login_required
def dive(request, dive_id):
    """
    Displays a single dive.
    """
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
    """
    View for editing dive data.
    """
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
    
def dive_add(request):
    """
    View for adding a new dive.
    """
    if request.method == 'POST':
        form = DiveForm(request.POST)
        form.instance.user = request.user
        form.instance.number = 1
        form.instance.size = 0
        
        # t = loader.get_template('divelog/debug_form.html')
        # c = RequestContext(request, {
            # 'form': form,
        # });
        # return HttpResponse(t.render(c))

        
        
        if form.is_valid():
            new_dive = form.save()
            
            messages.success(request, "New dive successfully saved with id #%d." % new_dive.id)
            return redirect('divelog.views.dive', dive_id = new_dive.id)
        else:
            messages.error(request, 'Failed saving dive.')
    else:
        form = DiveForm()
    
    t = loader.get_template('divelog/dive_add.html')
    c = RequestContext(request, {
        'form': form,
    });
    return HttpResponse(t.render(c))


@login_required
def profile(request):
    """
    Displays user's profile.
    """
    t = loader.get_template('accounts/profile.html')
    c = RequestContext(request);
    return HttpResponse(t.render(c))
